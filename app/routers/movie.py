from typing import Optional, List
from fastapi import HTTPException, status, Depends, APIRouter, Response
import models, schemas, oauth2
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix='/api/v1/movie',
    tags=['Movie APIs']
)


# Get Movie List
@router.get(
    path="/list/", 
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.MovieResponseSchema]
    )
def get_movies_list(
    db: Session = Depends(get_db), 
    limit: Optional[int] = 10,
    skip: Optional[int] = 0, 
    search: Optional[str] = "",
    ):
    results = db.query(models.MoviesModel).filter(
        models.MoviesModel.name.contains(search)).limit(limit).offset(skip).all()

    return results


# Get Movie with ID
@router.get(
    path="/{movie_id}/", 
    status_code=status.HTTP_200_OK, 
    response_model=schemas.MovieResponseSchema
    )
def get_movie(
    movie_id: int, 
    db: Session = Depends(get_db)
    ):
    result = db.query(models.MoviesModel).filter(models.MoviesModel.movie_id == movie_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Could not found movie with ID: {movie_id}"
            )
    return result


# Create Movie
@router.post(
    path='/create/'
    )
def create_movie(
    movie: schemas.MoviesSchema,
    db: Session = Depends(get_db), 
    user: models.UserModel = Depends(oauth2.get_current_admin_user)
    ):
    try:
        movie = models.MoviesModel(**movie.dict())
        db.add(movie)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error!! Movie Already Exists!"
        )
    return Response(status_code=status.HTTP_201_CREATED)


# Update Movie
@router.put(
    path='/update/{movie_id}/',
    response_model=schemas.MoviesSchema
    )
def update_movie(
    movie_id: int,
    movie: schemas.MoviesSchema,
    db: Session = Depends(get_db), 
    user: models.UserModel = Depends(oauth2.get_current_admin_user)
    ):
    query = db.query(models.MoviesModel).filter(models.MoviesModel.movie_id == movie_id)
    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Could not found movie with ID: {movie_id}"
            )

    query.update(movie.dict(), synchronize_session=False)
    db.commit()
    return query.first()


# Delete Movie
@router.delete(
    path='/delete/{movie_id}/'
    )
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db), 
    user: models.UserModel = Depends(oauth2.get_current_admin_user)
    ):
    query = db.query(models.MoviesModel).filter(models.MoviesModel.movie_id == movie_id)

    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Could not found movie with ID: {movie_id}"
            )

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)