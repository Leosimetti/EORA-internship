from fastapi import APIRouter, Request
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import CookieAuthentication
from pydantic import EmailStr
from typing import List
from .models import Bot
from .db import db

import os

SECRET = os.getenv("SECRET", "VERY133331235VERYsdad211SECRETPHRASENOONEKNOWS")


class User(models.BaseUser):
    bots: List[Bot] = []


class UserCreate(models.CreateUpdateDictModel):
    email: EmailStr
    password: str


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


collection = db["users"]
user_db = MongoDBUserDatabase(UserDB, db["users"])


async def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has been registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


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
router.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)

from fastapi import Depends, status


@router.post("/cheat-verify", status_code=status.HTTP_201_CREATED,
             responses={
             })
async def in_reality_it_should_be_done_via_email(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    await collection.update_one(
        {"id": user.id},
        {
            "$set": {
                "is_verified": True,
            }
        }
    )
    return user.is_verified
