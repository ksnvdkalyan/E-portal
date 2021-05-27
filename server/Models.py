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

class CheckIn(BaseModel):
    employeeNumber : str
    checkInImage : str

class CheckInDb(CheckIn,DBModelMixin):
    date: datetime = datetime.today().strftime('%Y%m%d')
    checkInTime: datetime = Field(default_factory=datetime.utcnow)
    checkOutImage : str = None
    checkOutTime :datetime =None

class applyLeave(BaseModel):
    startDate : str
    endDate : str
    appliedBy : str
    reason :str


class leaveInDB(applyLeave,DBModelMixin):
    manager: str
    status : str = 'Pending'
    createdTime : datetime = Field(default_factory=datetime.utcnow)

class holiday(BaseModel):
    Name : str
    date :datetime
class userLogin(BaseModel):
    username: str
    password: str

class updateLogin(userLogin):
    newpassword : str

class user(userLogin):
    firstName: str
    lastName: str
    DOB : str
    image : str

class userInDB(user,DBModelMixin):
    role: str
    manager : str = None
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)

class taskModel(BaseModel):
    task : str
    taskDescription : str
    username : str
    technology : str
    workLink : str
    
class taskInDB(taskModel,DBModelMixin):
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)
class deleteTask(BaseModel):
    username  : str
    id : str

class UpdateRole(BaseModel):
    groupName:str
class Role(BaseModel):
    groupName: str
    username:str
class RoleIndb(Role,DBModelMixin):
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)

class Group(BaseModel):
    groupName:str
    description:str
class GroupIndb(Group,DBModelMixin):
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)

class tokenResponse(BaseModel):
    token: str
    userName: str
    firstName: str
    lastName: str
    type: str
    role: str


class tokenRequest(BaseModel):
    userName: str
    password: str