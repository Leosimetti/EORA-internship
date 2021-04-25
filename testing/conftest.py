import pytest
import logging
import sys

from app.db import db
from fastapi.testclient import TestClient
from app.app import create_app

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


@pytest.fixture(scope="session")
def app():
    yield create_app()


@pytest.fixture(scope="function")
def temp_client(app):
    db.command("dropDatabase")
    yield TestClient(app)
    db.command("dropDatabase")


@pytest.fixture(scope="module")
def client(app):
    yield TestClient(app)


@pytest.fixture(scope="function")
def authorization_token(client):
    db.command("dropDatabase")
    client.post("/auth/register",
                json={
                    "email": "user@example.com",
                    "password": "string",
                })

    response = client.post("/auth/jwt/login",
                           data={
                               "username": "user@example.com",
                               "password": "string",
                               "grant_type": "",
                               "scope": "",
                               "client_id": "",
                               "client_secret": ""
                           })

    yield response.json()["access_token"]

    db.command("dropDatabase")
