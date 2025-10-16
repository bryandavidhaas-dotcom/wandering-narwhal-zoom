import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Force reload marker - updated to fix bcrypt issue
BCRYPT_FIX_VERSION = "1.0.1"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password using bcrypt directly.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to verify against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        # Handle bcrypt's 72-byte limit by truncating if necessary
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            logger.warning("Password longer than 72 bytes, truncating for bcrypt compatibility")
            password_bytes = password_bytes[:72]
        
        # Convert hashed password to bytes if it's a string
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(password_bytes, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt directly.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        str: The hashed password
        
    Raises:
        ValueError: If password hashing fails
    """
    try:
        # Handle bcrypt's 72-byte limit by truncating if necessary
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            logger.warning("Password longer than 72 bytes, truncating for bcrypt compatibility")
            password_bytes = password_bytes[:72]
        
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Password hashing failed: {e}")
        raise ValueError(f"Failed to hash password: {e}")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

security = HTTPBearer()

# Note: get_current_user() is now implemented in auth.py with proper database integration
# This mock version is kept for backward compatibility but should not be used