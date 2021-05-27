from pydantic import BaseModel, Field,validator
from datetime import datetime,date
from bson import ObjectId
from typing import List, Optional,Any

class DBModelMixin(BaseModel):
    id: Optional[Any] = Field(..., alias="_id")

    @validator("id")
    def validate_id(cls, id):
        return str(id)


class userLogin(BaseModel):
    username: str
    password: str

class updateLogin(userLogin):
    newpassword : str

class user(BaseModel):
    username: str
    password : str
    firstName: str
    lastName: str
    DOB : str
    image :str

class userInDB(user,DBModelMixin):
    role: str
    manager : str = None
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)