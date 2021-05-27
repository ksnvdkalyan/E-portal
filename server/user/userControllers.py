from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, MONGODB_DB_NAME
from Group.GroupModels import *
from user.userModel import *
import bcrypt
from passlib.hash import bcrypt
import asyncio
from pydantic import Field
import datetime


async def userDetails_get(username:str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    row = await collection.find_one({'username': username})
    user = userInDB(**row)
    return user

async def get_all_users():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    users = collection.find()
    group :List[userInDB] = []
    async for user in users:
        data = userInDB(**user)
        group.append(data)
    return group

async def add_users(users: user):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    row = await collection.find_one({"username": users.username})
    if row:
        print("User Already Exists")
    else:
        print("No User Exists")
        usr = {'_id':None,'image':users.image,'firstName': users.firstName, 'lastName': users.lastName, 'username': users.username, 'role': "user",
               'password': bcrypt.hash(users.password),'DOB':users.DOB}

        dbuser = userInDB(**usr)
        response = await collection.insert_one(dbuser.dict())

    return {'Message' : 'User added'}

async def delete_user(username:str,id : str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    row = await collection.find_one({"_id": ObjectId(id)})
    if row:
        if row['username'] == username or row['manager'] == username :
            raw = userInDB(**row)
            await collection.delete_one(raw.dict())
            return {'message' : 'user Deleted'}
    else:
        return {'message':'user doesnot exists'}


async def findUser(username: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    row = await collection.find_one({"username": username})
    if row:
        print("User Already Exists")
        usrdB = userInDB(**row)
        return usrdB
    else:
        return "No User"

async def get_usersById():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    users = collection.find()
    group :List[userInDB] = []
    ids = []
    async for user in users:
        ids.append(str(user['_id']))

    return ids

async def get_reporties(username: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    users = collection.find({"manager": username})
    groups: List[userInDB] = []
    userId = []
    async for document in users:
        data = userInDB(**document)

        groups.append(data)
    return groups

async def set_reportie(username : str ,reportieId : str ):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    row = await collection.find_one({"username":username})
    if row['role'] == "admin":

       raw = await collection.update_one({"_id":ObjectId(reportieId)}, {'$set': {'manager': username}})
       return {'message':'added reportie'}
    elif row['role'] == "Director":
        raw = await collection.update_one({"_id": ObjectId(reportieId)}, {'$set': {'role': "admin"}})
        return {'message': 'added reportie'}
    else:
        return {'message':'Acces Denied'}


async def set_admin_put(username : str ,reportieId : str ):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    row = await collection.find_one({"username":username})
    if row['role'] == "Director":

       raw = await collection.update_one({"_id":ObjectId(reportieId)}, {'$set': {'role': "admin"}})
       return {'message':'added admin user'}
    else:
        return {'message':'Acces Denied'}


async def remove_reportie_put(username : str ,reportieId : str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    row = await collection.find_one({"_id": ObjectId(reportieId)})
    if row :
        if row['manager'] == username:
            raw = await collection.update_one({"_id": ObjectId(reportieId)}, {'$set': {'manager': None}})
            return {'message': 'removed reportie'}
        else:
            return {'message':'Acess Denied'}
    else:
        return {'message': 'reportie doesnot exist'}