from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix='/api/v1/watchlist', 
    tags=["Watch List APIs"]
)


# Show Watchlist
@router.get(
    path='/show/',
    response_model=List[schemas.WatchListResponseSchema]
    )
def show_watchlist(
    db: Session = Depends(get_db), 
    user: models.UserModel = Depends(oauth2.get_current_user)
    ):
    data = db.query(models.MoviesModel.movie_id, models.MoviesModel.name).select_from(models.WatchListModel).join(
        models.MoviesModel, models.WatchListModel.movie_id==models.MoviesModel.movie_id, isouter=True).filter(
            models.WatchListModel.user_id==user.user_id).all()

    return data



# Add Movie into WatchList
@router.post(
    path='/add/'
    )
def add_movie(
    data: schemas.WatchListSchema,
    db: Session = Depends(get_db), 
    user: models.UserModel = Depends(oauth2.get_current_user)
    ):
    movie = db.query(models.MoviesModel).filter(models.MoviesModel.movie_id == data.movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Moive with ID {data.movie_id} does not exists"
        )

    try:
        data.user_id = user.user_id
        data = models.WatchListModel(**data.dict())
        db.add(data)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie is already in your WatchList"
            )
        
    return Response(status_code=status.HTTP_201_CREATED)



# Delete Movie from your Watch List
@router.delete(
    path='/remove/'
    )
def remove_movie(
    data: schemas.WatchListSchema,
    db: Session = Depends(get_db), 
    user: models.UserModel = Depends(oauth2.get_current_user)
    ):
    movie = db.query(models.WatchListModel).filter(
        models.WatchListModel.user_id == user.user_id,
        models.WatchListModel.movie_id == data.movie_id).delete(synchronize_session=False)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {data.movie_id} does not exist in your WatchList"
        )
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)