from pydantic import BaseModel, Field,validator
from datetime import datetime,date
from bson import ObjectId
from typing import List, Optional,Any


class DBModelMixin(BaseModel):
    id: Optional[Any] = Field(..., alias="_id")

    @validator("id")
    def validate_id(cls, id):
        return str(id)

class taskModel(BaseModel):
    task: str
    taskDescription: str
    username: str
    technology: str
    workLink: str


class taskInDB(taskModel, DBModelMixin):
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)