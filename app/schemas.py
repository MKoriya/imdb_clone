from pydantic import BaseModel, EmailStr, Extra, validator
from typing import Optional


# Movie Schemas
class MoviesSchema(BaseModel):
    name: str
    director: str
    popularity: float
    imdb_score: Optional[float] = 0
    genre: str

    class Config:
        orm_mode = True

    @validator("popularity")
    def validate_popularity(cls, v):
        if v < 1 or v > 100:
            raise ValueError("Popularity must be between 1 to 100")
        return v

    @validator('imdb_score')
    def validate_imdb_score(cls, v):
        if v < 1 or v > 10:
            raise ValueError("IMDB Score must be between 1 to 10") 
        return v

class MovieResponseSchema(BaseModel):
    movie_id: int
    name: str 
    director: str
    popularity: float
    imdb_score: float
    genre: str

    class Config:
        orm_mode = True



# User Schemas
class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        extra = Extra.allow

class UserResponseSchema(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str



# Auth Schemas
class CredentialsSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    user_id: int
    is_admin: bool



# Watch List
class WatchListSchema(BaseModel):
    movie_id: int

    class Config:
        extra = Extra.allow


class WatchListResponseSchema(BaseModel):
    movie_id: int
    name: str

    class Config:
        orm_mode = True