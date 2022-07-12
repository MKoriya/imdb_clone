from app import models

def test_create_movie(mock_login_admin, client):
    data = {"name": "test", "director": "dev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    res = client.post(
        "/api/v1/movie/create/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_admin['access_token']}"}
    )
    assert res.status_code == 201


def test_create_movie_no_auth(mock_login_admin, client):
    data = {"name": "test", "director": "dev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    res = client.post(
        "/api/v1/movie/create/",
        json=data,
    )
    assert res.status_code == 401


def test_create_movie_no_data(mock_login_admin, client):
    res = client.post(
        "/api/v1/movie/create/",
        headers={"Authorization": f"Bearer {mock_login_admin['access_token']}"}
    )
    assert res.status_code == 422


def test_update_movie(mock_movie, mock_login_admin, client):
    data = {"name": "test", "director": "pydev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    res = client.put(
        "/api/v1/movie/update/1/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_admin['access_token']}"}
    )
    new_data = res.json()
    assert new_data == data
    assert res.status_code == 200


def test_update_movie_wrong_id(mock_movie, mock_login_admin, client):
    data = {"name": "test", "director": "pydev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    res = client.put(
        "/api/v1/movie/update/2/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_admin['access_token']}"}
    )
    assert res.status_code == 404


def test_update_movie_no_auth(mock_movie, mock_login_admin, client):
    data = {"name": "test", "director": "pydev", "popularity": 80, "imdb_score": 9, "genre": "CS"}
    res = client.put(
        "/api/v1/movie/update/1/",
        json=data,
    )
    assert res.status_code == 401


def test_delete_movie_no_auth(mock_movie, mock_login_admin, client, session):
    res = client.delete(
        "/api/v1/movie/delete/1/"
    )
    assert res.status_code == 401


def test_delete_movie(mock_movie, mock_login_admin, client, session):
    res = client.delete(
        "/api/v1/movie/delete/1/",
        headers={"Authorization": f"Bearer {mock_login_admin['access_token']}"}
    )
    assert session.query(models.MoviesModel).get(1) == None
    assert res.status_code == 204


def test_delete_movie_wrong_id(mock_movie, mock_login_admin, client, session):
    res = client.delete(
        "/api/v1/movie/delete/2/",
        headers={"Authorization": f"Bearer {mock_login_admin['access_token']}"}
    )
    assert res.status_code == 404


def test_get_movie(mock_movie, client):
    res = client.get(
        "/api/v1/movie/1/"
    )
    data = res.json()
    assert data['movie_id'] == 1
    assert res.status_code == 200


def test_get_movie_wrong_id(mock_movie, client):
    res = client.get(
        "/api/v1/movie/2/"
    )
    assert res.status_code == 404


def test_empty_movie_list(client):
    res = client.get(
        "/api/v1/movie/list/"
    )
    assert res.json() == []
    assert res.status_code == 200


def test_movie_list(mock_movie_list, client):
    res = client.get(
        "/api/v1/movie/list/"
    )
    data = res.json()
    assert len(data) == len(mock_movie_list)
    assert res.status_code == 200


def test_movie_list_limit(mock_movie_list, client):
    res = client.get(
        "/api/v1/movie/list/?limit=1"
    )
    data = res.json()
    assert len(data) == 1
    assert data[0]['name'] == "test1"
    assert res.status_code == 200


def test_movie_list_limit_skip(mock_movie_list, client):
    res = client.get(
        "/api/v1/movie/list/?limit=1&skip=1"
    )
    data = res.json()
    assert len(data) == 1
    assert data[0]['name'] == "test2"
    assert res.status_code == 200


def test_movie_list_search(mock_movie_list, client):
    res = client.get(
        "/api/v1/movie/list/?search=test3"
    )
    data = res.json()
    assert len(data) == 1
    assert data[0]['name'] == "test3"
    assert res.status_code == 200