from pydantic import BaseModel, validator
import re
import requests
import os


class RegisterUser(BaseModel):
    email: str
    password: str


class BotFind(BaseModel):
    label: str

    @validator('label')
    def name_must_be_sufficient_length(cls, v):
        if len(v) > 55:
            raise ValueError("Label to long")
        return v


class Bot(BaseModel):
    label: str
    token: str

    @validator('label')
    def name_must_be_sufficient_length(cls, v):
        if len(v) > 55:
            raise ValueError("Label to long")
        return v

    @validator('token')
    def token_must_be_valid(cls, v):

        if os.getenv("HOST_IP") is not None:
            response = requests.get(f"https://api.telegram.org/bot{v}/getMe")
            if not response.json()["ok"]:
                raise ValueError("Invalid token")

        if re.fullmatch(r"^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$", v) is None:
            raise ValueError("Incorrect token format")
        return v

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.label == self.label or other.token == self.token
        else:
            return False
