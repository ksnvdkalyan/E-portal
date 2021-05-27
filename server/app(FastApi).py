import pprint
from fastapi import FastAPI,requests
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, MONGODB_DB_NAME
import asyncio
#from Models import *
from Group import *
from user import *
from Roles import *
from task import *
from leave import *
from starlette import status
from starlette.responses import JSONResponse
from passlib.hash import bcrypt
from fastapi.encoders import jsonable_encoder
from pydantic import Field
from passlib.context import CryptContext
import jwt
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from flask_cors import CORS
import datetime
from bson import ObjectId


pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

app = FastAPI(title= 'E-Portal',version='1.0')
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/today_BD')
async  def today_Birthday():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    date = datetime.date.today()
    today = date.strftime("%Y/%m/%d")
    print(today)
    bd = today[5:10]
    print("bd is " + bd)
    row =  collection.find({})
    hbd : List[userInDB] = []
    async for user in row:
            print(user["DOB"][5:10])
            if user["DOB"][5:10] == str(today[5:10]):
                data = userInDB(**user)
                hbd.append(data.dict())
                #hbd.append({'names':user["username"]})
            await asyncio.sleep(1)
    print(hbd)
    return hbd


@app.get('/month_BD')
async def month_BD():
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.get_database(MONGODB_DB_NAME)
        collection = db.get_collection("users")
        date = datetime.date.today()
        today =date.strftime("%y/%m/%d")
        month = date.strftime("%m")
        users = collection.find()
        month_bdname = []
        month_bdDate =[]
        async for user in users:
            if user['DOB'][5:7]==month and  user['DOB'][8:10]>str(date)[8:10]:
                month_bdname.append({'names': user['username']})
                month_bdDate.append({'date':user['DOB'][5:10]})

        return month_bdname,month_bdDate

@app.get('/Holidays')
async def Holidays():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Holidays")
    date = datetime.date.today()
    today = date.strftime("%y/%m/%d")
    month = date.strftime("%m")
    holidays = collection.find()
    month_holidayname = []
    month_holidayDate = []
    async for holiday in holidays:
        if holiday['Date'][5:7] == month and holiday['Date'][8:10] > str(date)[8:10]:
            month_holidayname.append({'names': holiday['Name']})
            month_holidayDate.append({'date': holiday['Date']})

    return month_holidayname, month_holidayDate

@app.post("/check_in",tags=['check-in'])
async def check_in_post(employeeNumber : str,checkInImage : str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("checkIn")
    check = { '_id': None ,'employeeNumber': employeeNumber ,'checkInImage':checkInImage}
    data = CheckInDb(**check)
    await collection.insert_one(data.dict())
    return {'message':'checked-in'}

@app.post("/check_out")
async def check_out_post(id : str,checkOutImage : str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("checkIn")
    row = await collection.find_one({'_id':ObjectId(id)})
    if row['checkOutTime'] == None:
        await collection.update_one({'_id':ObjectId(id)},{'$set':{'checkOutImage':checkOutImage,'checkOutTime':datetime.datetime.utcnow()}})
        return {'message':'checked-out'}
    else:
        return {'message':'Already checked-out'}
@app.get("/check_in_by_employeeNumber",tags=['check-in'])
async def check_in_by_employeeNumber_get(employeeNumber : str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("checkIn")
    record :List[CheckInDb] =[]
    row = collection.find({'employeeNumber':employeeNumber})
    async for item in row:
        data =CheckInDb(**item)
        record.append(data)
    return record

@app.get("/check_in",tags=['check-in'])
async def check_in_get():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("checkIn")
    record :List[CheckInDb] =[]
    row = collection.find({})
    async for item in row:
        data =CheckInDb(**item)
        record.append(data)
    return record


@app.post("/login", tags=["Login"])
async def login(login: userLogin):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    check = await collection.find_one({"username": login.username})
    if check:
        mpassword = check['password']
        print(mpassword)
        if bcrypt.verify(login.password, mpassword):
            token = jwt.encode(
                {'user': login.username, 'scope': 'user', 'iss': 'https://sangam.ai/',
                 'sub': 'Aryabhatta',
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                'SECRET_KEY')
            return {'username': login.username,
                    'firstName': check['firstName'],
                    'lastName': check['lastName'],
                    'token': token.decode('UTF-8'),
                    'image': check['image'],
                    'message': 'Authentication Success'}
        else:
            print("password Mismatch")
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Authentication Failed")
    else:
        print("user not found")
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Authentication Failed")
@app.put("/login",tags=['login'])
async def login_put(user:updateLogin):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    row = await collection.find_one({'username':user.username})
    if row:
        print("user exists")
        if bcrypt.verify(user.password, row['password']):
            raw = await collection.update_one({'username':user.username},{'$set':{'password':bcrypt.hash(user.newpassword)}})
            return {'message':'password updated'}
        else:
            print("Entered wrong password")
            return {'message':'password is invalid'}
    else:
        print("user desnot exist")
        return {'message':'user doesnot exist'}

@app.get("/userDetails", tags=['Users'])
async def userDetails_get(username: str):
    return await userControllers.userDetails_get(username)


@app.get("/all_users", tags=['Users'])
async def get_all_users():
    return await userControllers.get_all_users()


@app.post("/add_users", tags=['Users'])
async def add_users(users: user):
    return await userControllers.add_users(users)


@app.delete("/delete_user", tags=['Users'])
async def delete_user(username: str, id: str):

        return await userControllers.delete_user(username,id)


@app.get("/findUser", tags=['Users'])
async def findUser(username: str):
        return await userControllers.findUser(username)


@app.get("/usersById", tags=["Users"])
async def get_usersById():

    return await userControllers.get_usersById()


@app.post("/leave", tags=['Leave'])
async def add_leave_post(user: applyLeave):
        return await leaveControllers.add_leave_post(user)


@app.get("/leave", tags=['Leave'])
async def get_leaves_by_user(username: str):
    return await leaveControllers.get_leaves_by_user(username)


@app.get("/reporties_leave", tags=['Leave'])
async def get_reporties_leaves(username: str):
    return await leaveControllers.get_reporties_leaves(username)


@app.put("/approve_leave", tags=['Leave'])
async def approve_leave(username: str, requestId: str, message: str):
    return await leaveControllers.approve_leave(username,requestId,message)


@app.get("/get_TasksbyId", tags=['Tasks'])
async def get_Tasks(id: str, username: str):
    return await taskControllers.get_Tasks(id,username)


@app.get("/get_Tasks_byUser", tags=['Tasks'])
async def get_tasks_by_user(user: str):
    return await taskControllers.get_tasks_by_user(user)


@app.post("/add_Tasks", tags=['Tasks'])
async def add_Tasks(Tasks: taskModel):
    return await taskControllers.add_Tasks(Tasks)


@app.delete("/Tasks", tags=['Tasks'])
async def delete_tasks(username: str, id: str):
    return await taskControllers.delete_tasks(username,id)


@app.put("/Update_Tasks", tags=['Tasks'])
async def Update_Tasks(username: str, id: str, task: str, taskDescription: str, workLink: str, technology: str):
    return await taskControllers.Update_Tasks(username,id,task,taskDescription,workLink,technology)



@app.get("/get_reportiesTasks", tags=['Reporties'])
async def get_reportiesTask(username: str):
    return await taskControllers.get_reportiesTask(username)


@app.get("/get_reporties", tags=['Reporties'])
async def get_reporties(username: str):
    return await userControllers.get_reporties(username)


@app.get("/getA_reportiesTasks", tags=['Reporties'])
async def getA_reportiesTask(username: str, reportieId: str):
    return await taskControllers.getA_reportiesTask(username,reportieId)


@app.put("/set_reportie", tags=['Reporties'])
async def set_reportie(username: str, reportieId: str):
    return await userControllers.set_reportie(username,reportieId)


@app.put("/set_adminuser", tags=['Reporties'])
async def set_admin_put(username: str, reportieId: str):
    return await userControllers.set_admin_put(username,reportieId)


@app.put("/remove_reportie", tags=['Reporties'])
async def remove_reportie_put(username: str, reportieId: str):
    return await userControllers.remove_reportie_put(username,reportieId)


@app.get("/myGroups", tags=["Users"])
async def get_my_groups(username: str):
    return await groupControllers.get_my_groups(username)


@app.get("/groups", tags=["Groups"])
async def get_groups():
    return await groupControllers.get_groups()


@app.get("/groupById", tags=["Groups"])
async def get_group_by_id(id: str):
    return await groupControllers.get_group_by_id(id)


@app.get("/roles", tags=["Roles"])
async def get_roles():
    return await rolesControllers.get_roles()


@app.get("/rolesByGroup", tags=["Roles"])
async def get_roles_by_group(id: str):
    return await rolesControllers.get_roles_by_group(id)


@app.post("/groups", tags=["Groups"])
async def post_groups(data: Group):
    return await groupControllers.post_groups(data)


@app.post("/roles", tags=["Roles"])
async def post_roles(role: Role):
    return await rolesControllers.post_roles(role)


@app.put("/group", tags=["Groups"])
async def put_group(id: str, data: Group):
    return await groupControllers.put_group(id,data)


@app.put("/role", tags=["Roles"])
async def put_role(data: UpdateRole, id: str):
    return await rolesControllers.put_role(data,id)


@app.delete("/groups", tags=["Groups"])
async def delete_group(id: str):
    return await groupControllers.delete_group(id)


@app.delete("/roles", tags=["Roles"])
async def delete_role(id: str):
    return await rolesControllers.delete_role(id)




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)