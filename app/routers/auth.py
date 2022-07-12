from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
import schemas, models, utils, oauth2

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Authentication APIs']
)


@router.post(
    path='/login/', 
    response_model=schemas.TokenSchema
    )
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # get user from User Table
    user = db.query(models.UserModel).filter(models.UserModel.email==credentials.username).first()

    # raise exception if email/password is incorrect
    if not user or not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Generate access token
    access_token = oauth2.create_access_token(
        data={'user_id': user.user_id, 'is_admin': user.is_admin})

    return {"access_token": access_token, "token_type": "Bearer"}

