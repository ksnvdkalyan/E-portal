from pydantic import BaseModel, Field,validator
from datetime import datetime,date
from bson import ObjectId
from typing import List, Optional,Any


class DBModelMixin(BaseModel):
    id: Optional[Any] = Field(..., alias="_id")

    @validator("id")
    def validate_id(cls, id):
        return str(id)

class applyLeave(BaseModel):
    startDate : str
    endDate : str
    appliedBy : str
    reason :str


class leaveInDB(applyLeave,DBModelMixin):
    manager: str
    status : str = 'Pending'
    createdTime : datetime = Field(default_factory=datetime.utcnow)