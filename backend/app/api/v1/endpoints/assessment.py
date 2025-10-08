from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
import docx
from pypdf import PdfReader
import io
from app.models.assessment import UserAssessment
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase

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
    assessment_in: UserAssessment,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    db: AsyncIOMotorDatabase = request.app.mongodb
    assessment_data = assessment_in.dict()
    assessment_data["user_id"] = current_user["_id"]
    
    new_assessment = UserAssessment(**assessment_data)
    
    await db.assessments.insert_one(new_assessment.dict(by_alias=True))
    
    return new_assessment