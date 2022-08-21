from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends
import json
from database.hash import Hash
from database import models
import requests
from router import user
from database.models import Dbuser
from sqlalchemy import create_engine
from sqlalchemy.orm import Session ,sessionmaker
import pytest
import logging
from main import app, get_db
from database.db import get_test_db


#config

def drop_all(db):
    from database.models import Base as ModelsBase
    ModelsBase.metadata.drop_all(db.bind)

def override_get_db():
    try:
        db = get_test_db()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# def create_new user(username , password,is_admin):
#     test_db = get_test_db()
    

def test_create_user():
    test_db = get_test_db()
    test_db.add(Dbuser(
        username="ali",
        password=Hash.bcrypt("ali"),
        is_admin=False

    ))
    test_db.commit()
    response = client.post(
            "/login",
            json={
                "username":"ali",
                "password":"ali"
            },
        )
    drop_all(test_db)




token = {
        # "access_token": pytest_regex("^e.*\."),
        "type_token": "bearer"
}
def test_login_valid_user():
    test_db = get_test_db()
    test_db.add(Dbuser(
        username="ali",
        password=Hash.bcrypt("ali"),
        is_admin=False

    ))
    test_db.commit()
    response = client.post(
        "/login",
        json={
            "username":"ali",
            "password":"ali"
        },
    )

    assert response.status_code == 200
    assert "type_token" in response.json()
    drop_all(test_db)

def test_login_not_user():
    test_db = get_test_db()
    test_db.add(Dbuser(
        username="ali",
        password=Hash.bcrypt("ali"),
        is_admin=False
    ))
    test_db.commit()
    response = client.post(
        "/login",
        json={
            "username":"ali",
            "password":"123"
        }
    )

    assert response.status_code == 200
    assert "Not Vaild username or Poassword" in response.json()
    drop_all(test_db)
    

def test_login_sqlinj():
    test_db = get_test_db()
    test_db.add(Dbuser(
        username="ali",
        password=Hash.bcrypt("ali"),
        is_admin=False
    ))
    test_db.commit()
    response = client.post(
        "/login",
        json={
            "username": "sajjad';-- ",
            "password": "||sqlite_version()||"
        },
    )

    assert response.status_code == 200
    assert "Not Vaild username or Poassword" in response.json()
    drop_all(test_db)

def test_generate_valid_coupon():
    test_db = get_test_db()
    test_db.add(Dbuser(
        username="admin",
        password=Hash.bcrypt("admin"),
        is_admin=True
    ))
    test_db.commit()
    response =client.post(
        "/login",
        json={
            "username": "admin",
            "password": "admin"
        },
    )
    get_token = response.json().get("access_token")
    # std_handler = logging.StreamHandler()
    # std_handler.setLevel(logging.INFO)
    # logging.basicConfig(handlers=[std_handler], level=logging.DEBUG)
    # logging.info("sallam")
    generate_response = client.post(
        "/generate-coupon",
        headers={
            "Authrization" : get_token
        },
        json={"count": 3}
    )
    assert generate_response.status_code ==200
    assert "code" in generate_response.json()[0]

# def test_generate_coupon_no_token():
# def test_
