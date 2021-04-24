from fastapi import APIRouter, Request
from fastapi_users import FastAPIUsers, models
from pydantic import BaseConfig
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import CookieAuthentication
from typing import List
from .models import Bot
from .db import db

import json

SECRET = "VERY133331235VERYsdad211SECRETPHRASENOONEKNOWS"


class User(models.BaseUser):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            Bot: lambda b: json.dumps({"name": b.name, "token": b.token}),
        }

    bots: List[Bot] = []


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


collection = db["users"]
user_db = MongoDBUserDatabase(UserDB, db["users"])


async def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has been registered.")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)
cookie_authentication = CookieAuthentication(
    secret=SECRET, lifetime_seconds=3600, cookie_name="EORA-cookie"
)

router = APIRouter()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication, cookie_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_auth_router(cookie_authentication), prefix="/auth/cookie", tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
