from urllib.request import Request
from database.db import get_db
from urllib import response
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
import json
from main import app
from tests.conftest import session
# from router import user

client = TestClient(app)



def test_create_user(client):
    @app.route("/default")
    def make_user(db:session):
        assert response.status_code == 200


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()



token = {
        # "access_token": pytest_regex("^e.*\."),
        "type_token": "bearer"
}
def test_login_user():
    response = client.post(
        "/login",
        # headers={ 
        #     'accept: application/json', 
        #     'Content-Type: application/json'},
        json={
            "username":"sajjad",
            "password":"123"
        },
    )

    assert response.status_code == 200
    assert "type_token" in response.json()
def test_login_not_user():
    response = client.post(
        "/login",
        json={
            "username":"sajjad",
            "password":"wrongPass"
        },
    )

    assert response.status_code == 200
    assert "Not Vaild username or Poassword" in response.json()

def test_login_sqlinj():
    response = client.post(
        "/login",
        json={
            "username": "sajjad';-- ",
            "password": "||sqlite_version()||"
        },
    )

    assert response.status_code == 200
    assert "Not Vaild username or Poassword" in response.json()

# def test_generate_coupon():
#     get_token = response = client.get(
#         "/login",
#         json={
#             "username":"admin",
#             "password":"admin"
#         },
#     )
#     get_token = response.json()["access_token"]
#     response = client.post(
#         "/generate-coupon",
#         headers={
#             "Authrization" : get_token
#         }
#     )
#     assert response.status_code ==200
#     assert "code" in response.json()

def test_generate_coupon_no_token():
    pass
