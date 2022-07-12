from app import models

def test_get_empty_watchlist(mock_login_user, client):
    res = client.get(
        "/api/v1/watchlist/show/",
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}  
    )
    assert res.json() == []
    assert res.status_code == 200


def test_get_watchlist_no_auth(client):
    res = client.get(
        "/api/v1/watchlist/show/",
    )
    assert res.status_code == 401


def test_get_watchlist(mock_watchlist, mock_login_user, client):
    res = client.get(
        "/api/v1/watchlist/show/",
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}  
    )
    data = res.json()
    assert len(data) == len(mock_watchlist)
    assert res.status_code == 200


def test_add_movie(mock_movie, mock_login_user, client, session):
    data = {"movie_id": 1}
    res = client.post(
        "/api/v1/watchlist/add/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}  
    )
    assert res.status_code == 201


def test_add_movie_wrong_id(mock_movie, mock_login_user, client):
    data = {"movie_id": 2}
    res = client.post(
        "/api/v1/watchlist/add/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}  
    )
    assert res.status_code == 404


def test_add_movie_no_data(mock_movie, mock_login_user, client):
    res = client.post(
        "/api/v1/watchlist/add/",
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}  
    )
    assert res.status_code == 422


def test_add_movie_no_auth(mock_movie, mock_login_user, client):
    data = {"movie_id": 1}
    res = client.post(
        "/api/v1/watchlist/add/",
        json=data,
    )
    assert res.status_code == 401


def test_remove_movie(mock_watchlist, mock_login_user, client, session):
    data = {"movie_id": 1}
    res = client.delete(
        "/api/v1/watchlist/remove/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}  
    )
    assert len(session.query(models.WatchListModel).all()) < len(mock_watchlist)
    assert session.query(models.WatchListModel).filter(models.WatchListModel.movie_id==1).first() == None
    assert res.status_code == 204


def test_remove_movie_no_auth(mock_watchlist, client, session):
    data = {"movie_id": 1}
    res = client.delete(
        "/api/v1/watchlist/remove/",
        json=data,
    )
    assert res.status_code == 401


def test_remove_movie_no_data(mock_watchlist, mock_login_user, client, session):
    res = client.delete(
        "/api/v1/watchlist/remove/",
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}  
    )
    assert res.status_code == 422


def test_remove_movie_wrong_id(mock_watchlist, mock_login_user, client, session):
    data = {"movie_id": 5}
    res = client.delete(
        "/api/v1/watchlist/remove/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}  
    )
    assert res.status_code == 404

