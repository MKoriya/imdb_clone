from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Float, text, Boolean

class MoviesModel(Base):

    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(100), nullable=False)
    director = Column(String(100), server_default='', nullable=False)
    popularity = Column(Float(16, 2), server_default='0.00')
    imdb_score = Column(Float(16, 1), server_default='0.0') 
    genre = Column(String(200), server_default='')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class UserModel(Base):

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, server_default=text('FALSE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class WatchListModel(Base):

    __tablename__ = 'watchlist'

    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), primary_key=True)
