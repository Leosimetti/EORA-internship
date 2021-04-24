import unittest

import asynctest
import logging
import sys
from fastapi.testclient import TestClient
from app.app import app
import os

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