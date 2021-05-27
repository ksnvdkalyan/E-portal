from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, MONGODB_DB_NAME
from Group.GroupModels import *
from Roles.RolesModels import *
import asyncio
from pydantic import Field
import datetime


async def get_roles():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Roles")
    check = collection.find({})
    roles: List[RoleIndb] = []
    async for role in check:
        data = RoleIndb(**role)
        roles.append(data)
    return roles



async def get_roles_by_group(id: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    groupsCollection = db.get_collection("Groups")
    rolesCollection = db.get_collection("Roles")
    check = await groupsCollection.find_one({'_id': ObjectId(id)})
    if check:
        roles: List[RoleIndb] = []
        async for role in rolesCollection.find({}):
            data = RoleIndb(**role)
            if data.groupName == check['groupName']:
                roles.append(data)
        return roles
    else:
        return {'message': "Role Does Not Exist"}


async def post_roles(role: Role):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Roles")
    check = await collection.find_one({"group_name": role.groupName})
    if check:
        return {"message": "Already Exists"}
    else:
        newRoleData = {
            '_id': None,
            'groupName': role.groupName,
            'username': role.username}
        storingNewData = RoleIndb(**newRoleData)
        await collection.insert_one(storingNewData.dict())
        return {"message": "Role Added"}

async def put_role(data: UpdateRole, id: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Roles")
    check = await collection.find_one({'_id': ObjectId(id)})
    if check:
        await collection.update_one({'_id': ObjectId(id)}, {'$set': {'groupName': data.groupName}})
        return {'message': 'Role Modified'}
    else:
        return {'message': 'Role Does Not Exist'}


async def delete_role(id: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Roles")
    check = await collection.find_one({"_id": ObjectId(id)})
    if check:
        data = Role(**check)
        await collection.delete_one(data.dict())
        return {"message": "Role Deleted"}
    else:
        return {"message": "Role Does Not Exists"}