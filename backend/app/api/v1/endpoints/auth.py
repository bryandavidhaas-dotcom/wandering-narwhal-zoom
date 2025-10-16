from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from app.models.user import User
from app.models.token import Token, TokenData
from app.core.security import get_password_hash, verify_password, create_access_token
from motor.motor_asyncio import AsyncIOMotorDatabase
from jose import JWTError, jwt
from app.core.config import settings
from datetime import timedelta, datetime
import secrets

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

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
    user = await db.users.find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=User)
async def register_user(user_in: UserCreate, request: Request):
    # DEBUG: Log incoming registration data
    print(f"🔍 DEBUG: Registration attempt")
    print(f"🔍 DEBUG: Received email: '{user_in.email}' (length: {len(user_in.email)})")
    print(f"🔍 DEBUG: Email repr: {repr(user_in.email)}")
    print(f"🔍 DEBUG: Password length: {len(user_in.password)}")
    
    db: AsyncIOMotorDatabase = request.app.mongodb
    user = await db.users.find_one({"email": user_in.email})
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
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
        raise
    
    await db.users.insert_one(new_user.dict(by_alias=True))
    
    return new_user

@router.post("/login", response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    db: AsyncIOMotorDatabase = request.app.mongodb
    user = await db.users.find_one({"email": form_data.username})
    # Handle both 'password' and 'hashed_password' field names for compatibility
    password_field = user.get("password") or user.get("hashed_password") if user else None
    if not user or not verify_password(form_data.password, password_field):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password")
async def forgot_password(request_data: ForgotPasswordRequest, request: Request):
    """
    Send password reset token to user's email
    """
    db: AsyncIOMotorDatabase = request.app.mongodb
    user = await db.users.find_one({"email": request_data.email})
    
    if not user:
        # Don't reveal if email exists or not for security
        return {"message": "If the email exists, a password reset link has been sent"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    reset_expires = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    
    # Store reset token in database
    await db.users.update_one(
        {"email": request_data.email},
        {
            "$set": {
                "reset_token": reset_token,
                "reset_token_expires": reset_expires,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # In a real application, you would send an email here
    # For now, we'll just return the token (remove this in production!)
    return {
        "message": "If the email exists, a password reset link has been sent",
        "reset_token": reset_token  # Remove this in production!
    }

@router.post("/reset-password")
async def reset_password(request_data: ResetPasswordRequest, request: Request):
    """
    Reset user password using reset token
    """
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # Find user with valid reset token
    user = await db.users.find_one({
        "reset_token": request_data.token,
        "reset_token_expires": {"$gt": datetime.utcnow()}
    })
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )
    
    # Hash new password
    hashed_password = get_password_hash(request_data.new_password)
    
    # Update user password and clear reset token
    await db.users.update_one(
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
    )
    
    return {"message": "Password has been reset successfully"}

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """
    Change user password (requires current password)
    """
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    # Verify current password
    user = await db.users.find_one({"email": current_user["email"]})
    password_field = user.get("password") or user.get("hashed_password")
    
    if not verify_password(current_password, password_field):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )
    
    # Hash new password
    hashed_password = get_password_hash(new_password)
    
    # Update password
    await db.users.update_one(
        {"email": current_user["email"]},
        {
            "$set": {
                "hashed_password": hashed_password,
                "updated_at": datetime.utcnow(),
                "password_reset_required": False
            }
        }
    )
    
    return {"message": "Password changed successfully"}