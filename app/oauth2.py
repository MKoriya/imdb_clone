from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from config import settings


SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
EXPIRATION_TIME = settings.JWT_EXPIRATION_TIME

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


# Create JWT Access Token at time of the User Login
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


# Verify JWT Access Token as part of Authentication Flow
def verify_access_token(token: str) -> schemas.TokenDataSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get('user_id')
        is_admin: bool = payload.get('is_admin')

        if user_id == None or is_admin == None:
            raise credentials_exception
        token_data = schemas.TokenDataSchema(user_id=user_id, is_admin=is_admin)

    except JWTError:
        raise credentials_exception

    return token_data


# Authenticate Admin User using JWT access token
def get_current_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.UserModel:
    token = verify_access_token(token=token)
    if token.is_admin:
        user = db.query(models.UserModel).filter(models.UserModel.user_id==token.user_id).first()
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authenticated!",
            headers={"WWW-Authenticate": "Bearer"}
            )


# Authenticate User using JWT access token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.UserModel:
    token = verify_access_token(token=token)
    user = db.query(models.UserModel).filter(models.UserModel.user_id==token.user_id).first()
    return user