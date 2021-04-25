import unittest

import asynctest
import logging
import sys
from fastapi.testclient import TestClient
from app.app import app
import os
import json

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)
client = TestClient(app)


class APITestCase(asynctest.TestCase):

    def tearDown(self) -> None:
        logger.debug(self.tearDown.__name__)
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        logger.debug(cls.tearDownClass.__name__ + "\n")
        pass

    @classmethod
    def setUpClass(cls) -> None:
        logger.debug(cls.setUpClass.__name__)
        pass

    def setUp(self) -> None:
        logger.debug(self.setUp.__name__)
        pass

    def test_review_database_deletion(self):
        logger.debug(self.test_review_database_deletion.__name__)
        assert True

    def test_stuff_1(self):
        logger.debug(self.test_stuff_1.__name__)
        assert True

    def test_stuff_2(self):
        logger.debug(self.test_stuff_2.__name__)
        assert True


class AnotherTestCase(APITestCase):

    def test_another_testcase(self):
        logger.debug(self.test_another_testcase.__name__)
        assert True

    @classmethod
    def tearDownClass(cls) -> None:
        logger.debug(cls.tearDownClass.__name__ + "\n")
        os._exit(0)


class TestConnection(asynctest.TestCase):

    async def test_db_connection(self):
        from app.db import DATABASE_URL
        import motor.motor_asyncio

        db_connection = motor.motor_asyncio.AsyncIOMotorClient(
            DATABASE_URL, uuidRepresentation="standard"
        )
        await db_connection["test"].test_collection.find_one()
        db_connection.close()


class TestBots(unittest.TestCase):
    from app.db import db

    token = ""
    prefix = "/bots"
    add_endpoint = prefix + "/add"
    list_endpoit = prefix + "/list"

    def setUp(self) -> None:
        self.db.command("dropDatabase")
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
        self.token = response.json()["access_token"]

    def test_add_one(self):
        bot = {"name": "CoolBot", "token": "1466"}

        response = client.post(self.add_endpoint,
                               headers={"Authorization": f"Bearer {self.token}"},
                               json=bot)
        assert response.status_code == 201, f"{response.status_code} : {response.text}"

        response = client.post(self.list_endpoit,
                               headers={"Authorization": f"Bearer {self.token}"})

        result = json.loads(response.text)
        assert len(result) == 1,f"Bots added {len(result)} instead of 1"

        resulting_bot = result[0]
        assert resulting_bot == bot, f"Expected {bot}, But got {resulting_bot}"

    def test_duplicate(self):
        client.post(self.add_endpoint,
                    headers={"Authorization": f"Bearer {self.token}"},
                    json={"name": "bot", "token": "1466"})
        response = client.post(self.add_endpoint,
                               headers={"Authorization": f"Bearer {self.token}"},
                               json={"name": "sas", "token": "1466"})

        assert response.status_code == 409, f"{response.status_code} : {response.text}"

    def test_more_than_five(self):
        for i in range(5):
            response = client.post(self.add_endpoint,
                                   headers={"Authorization": f"Bearer {self.token}"},
                                   json={"name": f"{i}", "token": f"{i}"})
            assert response.status_code == 201, f"{response.status_code} : {response.text}"

        response = client.post(self.add_endpoint,
                               headers={"Authorization": f"Bearer {self.token}"},
                               json={"name": "aboba", "token": "1222"})
        assert response.status_code == 403, f"{response.status_code} : {response.text}"

    def tearDown(self) -> None:
        self.db.command("dropDatabase")


class TestRegistration(unittest.TestCase):
    from app.db import db

    def setUp(self) -> None:
        self.db.command("dropDatabase")

    def tearDown(self) -> None:
        self.db.command("dropDatabase")

    def test_register_user(self):
        response = client.post("/auth/register",
                               json={
                                   "email": "user@example.com",
                                   "password": "string",
                               })
        assert response.status_code == 201

    def test_duplicate_register_user(self):
        response = client.post("/auth/register",
                               json={
                                   "email": "user@example.com",
                                   "password": "string",
                               })
        assert response.status_code == 201

        response = client.post("/auth/register",
                               json={
                                   "email": "user@example.com",
                                   "password": "string",
                               })
        assert response.status_code == 400

    def test_invalid_submission(self):
        response = client.post("/auth/register",
                               json={
                                   "email": "user.com",
                                   "password": "string",
                               })
        assert response.status_code == 422

        response = client.post("/auth/register",
                               json={
                                   "email": "user@example.com"
                               })
        assert response.status_code == 422
