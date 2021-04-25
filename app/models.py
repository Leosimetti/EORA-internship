from pydantic import BaseModel, BaseConfig, ValidationError, validator
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
import re


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class MongoModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }

    @classmethod
    def from_mongo(cls, data: dict):
        """We must convert _id into "id". """
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed


class Bot(MongoModel):
    label: str
    token: str

    @validator('label')
    def name_must_be_sufficient_length(cls, v):
        if len(v) > 55:
            raise ValueError("Label to long")
        return v

    @validator('token')
    def token_must_be_valid(cls, v):

        #TODO https://api.telegram.org/botYOURTOKEN/getMe

        if re.fullmatch(r"^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$", v) is None:
            raise ValueError("Incorrect token format")
        return v

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.label == self.label or other.token == self.token
        else:
            return False
