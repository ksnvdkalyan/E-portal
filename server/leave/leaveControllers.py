from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, MONGODB_DB_NAME
from Group.GroupModels import *
from leave.leaveModel import *
import asyncio
from pydantic import Field
import datetime

async def add_leave_post(user:applyLeave):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("leaves")
    userCollection =db.get_collection("users")
    raw = await userCollection.find_one({'username':user.appliedBy})
    leave = await collection.find_one({'appliedBy': user.appliedBy})
    if raw:
        userdetails = userInDB(**raw)
        leaveRequest = {'_id':None,'startDate':user.startDate,'endDate':user.endDate,'manager':userdetails.manager,
                 'appliedBy':user.appliedBy,'reason':user.reason}
        Request = leaveInDB(**leaveRequest)
        responce = await collection.insert_one(Request.dict())
        return {'message':'Request sent'}

async def get_leaves_by_user(username:str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("leaves")
    leaves = collection.find({'appliedBy': username})
    leaverequests : List[leaveInDB] = []
    if leaves:
        async for leave in leaves:
            data = leaveInDB(**leave)
            leaverequests.append(data.dict())

        return leaverequests

async def get_reporties_leaves(username:str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("leaves")
    leaves = collection.find({'manager': username})
    leaverequests : List[leaveInDB] = []
    if leaves:
        async for leave in leaves:
            data = leaveInDB(**leave)
            leaverequests.append(data.dict())

        return leaverequests

async def approve_leave(username:str,requestId:str,message:str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("leaves")
    print(requestId)
    leaves = await collection.find_one({'_id': ObjectId(requestId)})
    if leaves:
        print("in if")
        if leaves['manager'] == username:
            await collection.update_one({'_id': ObjectId(requestId)}, {'$set': {'status': message}})
            return {'message':'Request '+message}
        else:
            return {'message':'Access Denied'}
    else:
        return {'message':'Request not found'}