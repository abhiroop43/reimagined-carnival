import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

from app.dto.py_object_id import PyObjectId


class CandidateDto(BaseModel):
    id: str
    name: str
    email: EmailStr
    cv_received_date: datetime.datetime
    availability_in: int
    active: Optional[bool]
    created_on: Optional[datetime.datetime]
    created_by: Optional[str]
    updated_on: Optional[datetime.datetime]
    updated_by: Optional[str]


class CandidateModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    # _id: PyObjectId = Field(default_factory=PyObjectId)
    name: str = Field(...)
    email: EmailStr = Field(...)
    cv_received_date: datetime.datetime = Field(...)
    availability_in: int = Field(...)
    active: Optional[bool] = Field(default=True)
    created_on: Optional[datetime.datetime] = Field()
    created_by: Optional[str] = Field()
    updated_on: Optional[datetime.datetime] = Field()
    updated_by: Optional[str] = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Abhiroop Santra",
                "email": "abhiroop.santra@example.com",
                "cv_received_date": "2022-04-10T09:54:54.553570",
                "availability_in": 30,
            }
        }


class UpdateCandidateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    cv_received_date: datetime.datetime = Field(...)
    availability_in: int = Field(...)
    active: Optional[bool] = Field(default=True)
    created_on: Optional[datetime.datetime] = Field()
    created_by: Optional[str] = Field()
    updated_on: Optional[datetime.datetime] = Field()
    updated_by: Optional[str] = Field()

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
