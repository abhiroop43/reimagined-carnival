import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

from app.dto.py_object_id import PyObjectId


class CandidateModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    name: str = Field(...)

    email: EmailStr = Field(...)

    cv_received_date: datetime.date = Field(...)

    availability_in: int = Field(...)

    class Config:
        allow_population_by_field_name = True

        arbitrary_types_allowed = True

        json_encoders = {ObjectId: str}

        schema_extra = {

            "example": {

                "name": "Abhiroop Santra",

                "email": "abhiroop.santra@example.com",

                "cv_received_date": "2022-03-19",

                "availability_in": "30",

            }

        }
