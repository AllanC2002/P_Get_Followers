import os
import pytest
from unittest.mock import patch, MagicMock
from main import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    return flask_app.test_client()

@patch("services.functions.conection_userprofile")
@patch("main.jwt.decode")
def test_get_followers_success(mock_jwt_decode, mock_conection, client):
    # Simulate JWT decode
    mock_jwt_decode.return_value = {"user_id": 1}
    os.environ["SECRET_KEY"] = "test-secret-key"

    # Simulate database connection
    mock_session = MagicMock()
    mock_conection.return_value = mock_session

    # Simulate user profile active in database
    mock_profile = MagicMock()
    mock_profile.Id_User = 1
    mock_session.query().filter_by().first.return_value = mock_profile

    # Simulate followers in database
    follower1 = MagicMock(Id_User=2, User_mail="seguidor1@mail.com")
    follower2 = MagicMock(Id_User=3, User_mail="seguidor2@mail.com")
    mock_session.query().join().filter().all.return_value = [follower1, follower2]

    # execute the request
    response = client.get(
        "/followers",
        headers={"Authorization": "Bearer test.jwt.token"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "followers" in data
    assert isinstance(data["followers"], list)
    assert len(data["followers"]) == 2
    assert data["followers"][0]["User_mail"] == "seguidor1@mail.com"
