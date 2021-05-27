from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, MONGODB_DB_NAME
from Group.GroupModels import *
import asyncio
from pydantic import Field
import datetime
from bson import ObjectId

async def get_my_groups(username: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    rolesCollection = db.get_collection("Roles")
    myGroups = rolesCollection.find({'username': username})
    groups: List[Role] = []
    async for group in myGroups:
        data = Role(**group)
        groups.append(data)
    return groups



async def get_groups():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Groups")
    check = collection.find({})
    groups: List[GroupIndb] = []
    async for group in check:
        data = GroupIndb(**group)
        groups.append(data)
    return groups



async def get_group_by_id(id: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Groups")
    check = await collection.find_one({'_id': ObjectId(id)})
    if check:
        data = GroupIndb(**check)
        return data
    else:
        return {'message': "Group Does Not Exist"}


async def post_groups(data: Group):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Groups")
    check = await collection.find_one({"groupName": data.groupName})
    if check:
        return {"message": "Already Exists"}
    else:
        newGroupData = {
            '_id': None,
            'groupName': data.groupName,
            'description': data.description
        }
        storingNewData = GroupIndb(**newGroupData)
        await collection.insert_one(storingNewData.dict())
        return {"message": "Group Added"}


async def put_group(id: str, data: Group):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Groups")
    row = await collection.find_one({'_id': ObjectId(id)})
    if row:
        await collection.update_one({'_id': ObjectId(id)},
                                    {'$set': {'groupName': data.groupName,
                                              'description': data.description}})
        return {'message': 'Group Modified'}
    else:
        return {'message': 'Group Does Not Exist'}


async def delete_group(id: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Groups")
    check = await collection.find_one({"_id": ObjectId(id)})
    if check:
        data = Group(**check)
        await collection.delete_one(data.dict())
        return {"message": "Group Deleted"}
    else:
        return {"message": "Group Does Not Exists"}