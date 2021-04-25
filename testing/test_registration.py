# class TestRegistration:
#     from app.db import db
#
#     def setUp(self) -> None:
#         self.db.command("dropDatabase")
#
#     def tearDown(self) -> None:
#         self.db.command("dropDatabase")
#
#     def test_register_user(self):
#         response = client.post("/auth/register",
#                                json={
#                                    "email": "user@example.com",
#                                    "password": "string",
#                                })
#         assert response.status_code == 201
#
#     def test_duplicate_register_user(self):
#         response = client.post("/auth/register",
#                                json={
#                                    "email": "user@example.com",
#                                    "password": "string",
#                                })
#         assert response.status_code == 201
#
#         response = client.post("/auth/register",
#                                json={
#                                    "email": "user@example.com",
#                                    "password": "string",
#                                })
#         assert response.status_code == 400
#
#     def test_invalid_submission(self):
#         response = client.post("/auth/register",
#                                json={
#                                    "email": "user.com",
#                                    "password": "string",
#                                })
#         assert response.status_code == 422
#
#         response = client.post("/auth/register",
#                                json={
#                                    "email": "user@example.com"
#                                })
#         assert response.status_code == 422