from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
import docx
from pypdf import PdfReader
import io
from app.models.assessment import UserAssessment
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type == "application/pdf":
        try:
            pdf_stream = io.BytesIO(await file.read())
            reader = PdfReader(pdf_stream)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return {"text": text}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF file: {e}")
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            docx_stream = io.BytesIO(await file.read())
            doc = docx.Document(docx_stream)
            text = "\n".join([para.text for para in doc.paragraphs])
            return {"text": text}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing DOCX file: {e}")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or DOCX file.")

@router.post("/submit-assessment", response_model=UserAssessment)
async def submit_assessment(
    assessment_data: dict,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # Automatically set user_id from authenticated user
    assessment_data["user_id"] = current_user["_id"]
    assessment_data["_id"] = str(ObjectId()) if "_id" not in assessment_data else assessment_data["_id"]
    
    # Create UserAssessment object
    new_assessment = UserAssessment(**assessment_data)
    
    await db.assessments.insert_one(new_assessment.dict(by_alias=True))
    
    return new_assessment

@router.get("/get-latest-assessment")
async def get_latest_assessment(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    assessment = await db.assessments.find_one(
        {"user_id": current_user["_id"]},
        sort=[("created_at", -1)]
    )
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No assessment found for the current user.")
        
    return assessment