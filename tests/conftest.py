import pytest
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.utils import get_password_hash
from app import models

DATABASE_URL = settings.SQL_DATABASE_URL
SQLALCHEMY_DATABASE_URL = DATABASE_URL + "_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    def mock_password_hash(password):
        return password

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_password_hash] = mock_password_hash
    yield TestClient(app)



@pytest.fixture
def mock_user(session):
    user_data = {"name": "test", "email": "test@gmail.com", "password": "123"}
    hashed_password = get_password_hash(user_data["password"])
    user_data["password"] = hashed_password
    user = models.UserModel(**user_data)
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def mock_login_user(mock_user, client):
    data = client.post(
        "/api/v1/auth/login/", 
        data={"username": "test@gmail.com", "password": "123"}
    )
    assert data.status_code == 200
    return data.json()


@pytest.fixture
def mock_admin(session):
    admin_data = {"name": "test", "email": "test@gmail.com", "password": "123", "is_admin": True}
    hashed_password = get_password_hash(admin_data["password"])
    admin_data["password"] = hashed_password
    user = models.UserModel(**admin_data)
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def mock_login_admin(mock_admin, client):
    data = client.post(
        "/api/v1/auth/login/", 
        data={"username": "test@gmail.com", "password": "123"}
    )
    assert data.status_code == 200
    return data.json()


@pytest.fixture
def mock_movie(session):
    data = {"name": "test", "director": "dev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    movie = models.MoviesModel(**data)
    session.add(movie)
    session.commit()
    return movie


@pytest.fixture
def mock_movie_list(session):
    movies = []
    data = {"name": "test1", "director": "dev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    movie = models.MoviesModel(**data)
    movies.append(movie)
    session.add(movie)
    data = {"name": "test2", "director": "dev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    movie = models.MoviesModel(**data)
    movies.append(movie)
    session.add(movie)
    data = {"name": "test3", "director": "dev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    movie = models.MoviesModel(**data)
    movies.append(movie)
    session.add(movie)
    session.commit()
    return movies


@pytest.fixture
def mock_watchlist(mock_user, mock_movie_list, session):
    watchlist = []
    for movie in mock_movie_list:
        data = models.WatchListModel(**{"user_id": mock_user.user_id, "movie_id": movie.movie_id})
        watchlist.append(data)
        session.add(data)
    session.commit()
    return watchlist
