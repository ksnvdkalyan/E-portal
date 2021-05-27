from pydantic import BaseModel, Field,validator
from datetime import datetime,date
from bson import ObjectId
from typing import List, Optional,Any
import pytz
from pytz import timezone
tz = pytz.timezone('Asia/Kolkata')
class DBModelMixin(BaseModel):
    id: Optional[Any] = Field(..., alias="_id")

    @validator("id")
    def validate_id(cls, id):
        return str(id)

class UpdateRole(BaseModel):
    groupName:str
class Role(BaseModel):
    groupName: str
    username:str
class RoleIndb(Role,DBModelMixin):
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)