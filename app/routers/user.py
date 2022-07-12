import schemas, models, utils, oauth2
from database import get_db
from fastapi import HTTPException, Depends, status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/api/v1/user",
    tags=['User APIs']
)

# User APIs
@router.get(
    path='/{user_id}/',
    response_model=schemas.UserResponseSchema
)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    user: models.UserModel = Depends(oauth2.get_current_user)
    ):
    if user.user_id == user_id or user.is_admin:
        data = db.query(models.UserModel).filter(models.UserModel.user_id == user_id).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error!! Not Authorized"
            )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error!! User with ID {user_id} does not exists!!")
    return data


# Create User 
@router.post(
    path="/create/",
)
def create_user(
    user: schemas.UserSchema, 
    db: Session = Depends(get_db),
    ):
    try:
        hashed_password = utils.get_password_hash(user.password)
        user.password = hashed_password
        user = models.UserModel(**user.dict())
        db.add(user)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error!! Email is already in Use"
        )
    return Response(status_code=status.HTTP_201_CREATED)


# Create Admin User
@router.post(
    path='/create/admin/'
    )
def create_admin(
    user: schemas.UserSchema, 
    db: Session = Depends(get_db),
    admin: models.UserModel = Depends(oauth2.get_current_admin_user)
    ):
    try:
        hashed_password = utils.get_password_hash(user.password)
        user.password = hashed_password
        user.is_admin = True
        user = models.UserModel(**user.dict())
        db.add(user)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error!! Email is already in Use"
        )
    return Response(status_code=status.HTTP_201_CREATED)


# Delete User
@router.delete(
    path='/delete/{user_id}/'
    )
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: models.UserModel = Depends(oauth2.get_current_user)
    ):
    if user.user_id == user_id or user.is_admin:
        query = db.query(models.UserModel).filter(models.UserModel.user_id==user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error!! Not Authorized"
            )
    
    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error!! User with ID {user_id} does not exists!!")
    
    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Change Password
@router.put(
    path='/change_password/'
    )
def change_password(
    passwords: schemas.ChangePasswordSchema,
    db: Session = Depends(get_db),
    user: models.UserModel = Depends(oauth2.get_current_user)
    ):
    if utils.verify_password(passwords.old_password, user.password):
        new_hashed_password = utils.get_password_hash(passwords.new_password)
        db.query(models.UserModel).filter(models.UserModel.user_id==user.user_id).update(
            {models.UserModel.password: new_hashed_password}, synchronize_session=False
        )
        db.commit() 
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password Does not Match"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)