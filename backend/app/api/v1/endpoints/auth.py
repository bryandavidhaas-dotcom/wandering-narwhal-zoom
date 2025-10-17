from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, validator
from app.models.user import User
from app.models.token import Token, TokenData, TokenWithAssessment
from app.core.security import get_password_hash, verify_password, create_access_token
from motor.motor_asyncio import AsyncIOMotorDatabase
from jose import JWTError, jwt
from app.core.config import settings
from datetime import timedelta, datetime
import secrets
import asyncio
import re
from contextlib import asynccontextmanager

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database operation timeout configuration
DB_OPERATION_TIMEOUT = 10.0  # 10 seconds timeout for database operations

@asynccontextmanager
async def db_operation_context(db: AsyncIOMotorDatabase, operation_name: str):
    """Context manager for database operations with timeout and error handling"""
    try:
        print(f"🔄 Starting database operation: {operation_name}")
        yield db
        print(f"✅ Completed database operation: {operation_name}")
    except asyncio.TimeoutError:
        print(f"⏰ Database operation timeout: {operation_name}")
        raise HTTPException(
            status_code=503,
            detail=f"Database operation timed out: {operation_name}"
        )
    except Exception as e:
        print(f"❌ Database operation failed: {operation_name} - {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database operation failed: {operation_name}"
        )

async def safe_db_operation(coro, operation_name: str, timeout: float = DB_OPERATION_TIMEOUT):
    """Wrapper for database operations with timeout handling"""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        print(f"⏰ Database operation timeout: {operation_name}")
        raise HTTPException(
            status_code=503,
            detail=f"Database operation timed out: {operation_name}"
        )
    except Exception as e:
        print(f"❌ Database operation failed: {operation_name} - {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database operation failed: {operation_name}"
        )

def validate_password_strength(password: str) -> str:
    """
    Validate password strength requirements
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")
    
    return password

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        return validate_password_strength(v)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        return validate_password_strength(v)

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    db: AsyncIOMotorDatabase = request.app.mongodb
    async with db_operation_context(db, "get_current_user"):
        user = await safe_db_operation(
            db.users.find_one({"email": token_data.email}),
            "find_user_by_email"
        )
        if user is None:
            raise credentials_exception
        return user

@router.post("/register", response_model=TokenWithAssessment)
async def register_user(user_in: UserCreate, request: Request):
    # DEBUG: Log incoming registration data
    print(f"🔍 DEBUG: Registration attempt")
    print(f"🔍 DEBUG: Received email: '{user_in.email}' (length: {len(user_in.email)})")
    print(f"🔍 DEBUG: Email repr: {repr(user_in.email)}")
    print(f"🔍 DEBUG: Password length: {len(user_in.password)}")
    
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    try:
        async with db_operation_context(db, "register_user"):
            # Check if user already exists
            user = await safe_db_operation(
                db.users.find_one({"email": user_in.email}),
                "check_existing_user"
            )
            if user:
                raise HTTPException(
                    status_code=400,
                    detail="The user with this email already exists in the system.",
                )
    except HTTPException as e:
        if e.status_code == 400:
            raise e
        # Convert other HTTP exceptions to 400 for registration failures
        raise HTTPException(
            status_code=400,
            detail="Registration failed. Please try again.",
        )
    
    hashed_password = get_password_hash(user_in.password)
    user_data = user_in.dict()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]
    
    print(f"🔍 DEBUG: About to create User with data: {user_data}")
    
    try:
        new_user = User(**user_data)
        print(f"🔍 DEBUG: User model created successfully")
    except Exception as e:
        print(f"🔍 DEBUG: User model creation failed: {e}")
        print(f"🔍 DEBUG: Error type: {type(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user: {str(e)}"
        )
    
    async with db_operation_context(db, "insert_new_user"):
        # Insert new user with timeout
        await safe_db_operation(
            db.users.insert_one(new_user.dict(by_alias=True)),
            "insert_new_user"
        )
    
    # Automatically generate access token for the new user
    try:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_user.email}, expires_delta=access_token_expires
        )
        print(f"🔍 DEBUG: Access token generated successfully for user: {new_user.email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "assessment_completed": False  # New users haven't completed assessment yet
        }
    except Exception as e:
        print(f"🔍 DEBUG: Token generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="User created successfully but failed to generate access token"
        )

@router.post("/login", response_model=TokenWithAssessment)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    try:
        async with db_operation_context(db, "login_user"):
            user = await safe_db_operation(
                db.users.find_one({"email": form_data.username}),
                "find_user_for_login"
            )
            # Handle both 'password' and 'hashed_password' field names for compatibility
            password_field = user.get("password") or user.get("hashed_password") if user else None
            if not user or not verify_password(form_data.password, password_field):
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
    except HTTPException as e:
        if e.status_code == 401:
            raise e
        # Convert other HTTP exceptions to 401 for authentication failures
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user has completed assessment
    assessment_completed = False
    try:
        async with db_operation_context(db, "check_user_assessment"):
            assessment = await safe_db_operation(
                db.assessments.find_one({"user_id": user["_id"]}),
                "find_user_assessment",
                timeout=5.0  # Shorter timeout for assessment check
            )
            assessment_completed = assessment is not None
            print(f"🔍 DEBUG: Assessment check for user {user['email']}: {'completed' if assessment_completed else 'not completed'}")
    except Exception as e:
        print(f"⚠️  Assessment status check failed for user {user['email']}: {str(e)}")
        # Don't fail login if assessment check fails, just assume not completed
        assessment_completed = False
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "assessment_completed": assessment_completed
    }

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password")
async def forgot_password(request_data: ForgotPasswordRequest, request: Request):
    """
    Send password reset token to user's email
    """
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    async with db_operation_context(db, "forgot_password"):
        user = await safe_db_operation(
            db.users.find_one({"email": request_data.email}),
            "find_user_for_reset"
        )
        
        if not user:
            # Don't reveal if email exists or not for security
            return {"message": "If the email exists, a password reset link has been sent"}
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        reset_expires = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        
        # Store reset token in database
        await safe_db_operation(
            db.users.update_one(
                {"email": request_data.email},
                {
                    "$set": {
                        "reset_token": reset_token,
                        "reset_token_expires": reset_expires,
                        "updated_at": datetime.utcnow()
                    }
                }
            ),
            "update_reset_token"
        )
    
    # In a real application, you would send an email here
    # TODO: Implement email sending service
    print(f"🔐 Password reset token for {request_data.email}: {reset_token}")  # For development only
    
    return {
        "message": "If the email exists, a password reset link has been sent"
    }

@router.post("/reset-password")
async def reset_password(request_data: ResetPasswordRequest, request: Request):
    """
    Reset user password using reset token
    """
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    try:
        async with db_operation_context(db, "reset_password"):
            # Find user with valid reset token
            user = await safe_db_operation(
                db.users.find_one({
                    "reset_token": request_data.token,
                    "reset_token_expires": {"$gt": datetime.utcnow()}
                }),
                "find_user_with_reset_token"
            )
            
            if not user:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid or expired reset token"
                )
    except HTTPException as e:
        if e.status_code == 400:
            raise e
        # Convert other HTTP exceptions to 400 for invalid token
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )
        
        # Hash new password
        hashed_password = get_password_hash(request_data.new_password)
        
        # Update user password and clear reset token
        await safe_db_operation(
            db.users.update_one(
                {"_id": user["_id"]},
                {
                    "$set": {
                        "hashed_password": hashed_password,
                        "updated_at": datetime.utcnow(),
                        "password_reset_required": False
                    },
                    "$unset": {
                        "reset_token": "",
                        "reset_token_expires": ""
                    }
                }
            ),
            "update_password_and_clear_token"
        )
    
    return {"message": "Password has been reset successfully"}

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        return validate_password_strength(v)

@router.post("/change-password")
async def change_password(
    request_data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """
    Change user password (requires current password)
    """
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    async with db_operation_context(db, "change_password"):
        # Verify current password
        user = await safe_db_operation(
            db.users.find_one({"email": current_user["email"]}),
            "find_user_for_password_change"
        )
        password_field = user.get("password") or user.get("hashed_password")
        
        if not verify_password(request_data.current_password, password_field):
            raise HTTPException(
                status_code=400,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        hashed_password = get_password_hash(request_data.new_password)
        
        # Update password
        await safe_db_operation(
            db.users.update_one(
                {"email": current_user["email"]},
                {
                    "$set": {
                        "hashed_password": hashed_password,
                        "updated_at": datetime.utcnow(),
                        "password_reset_required": False
                    }
                }
            ),
            "update_user_password"
        )
    
    return {"message": "Password changed successfully"}