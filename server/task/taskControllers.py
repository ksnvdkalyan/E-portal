from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, MONGODB_DB_NAME
from Group.GroupModels import *
from task.taskModel import *
import datetime

async def get_Tasks(id: str, username: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database("ps2")
    collection = db.get_collection("appTask")
    row = await collection.find_one({'_id': ObjectId(id)})
    if row:
        if row['username'] == username:
            print('Task Exists')
            tasks = taskInDB(**row)
            return tasks
    else:
        print('Task Doesnot Exists')
        return {'message': "Task doesn't exist "}


async def get_tasks_by_user(user: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database("ps2")
    collection = db.get_collection("appTask")
    row = collection.find()
    tasksList: List[taskInDB] = []
    taskId = []
    tasks = []
    if row:
        print('Task Exists')
        async for task in row:
            if task['username'] == user:
                print(task)
                data = taskInDB(**task)
                print(data)
                tasks.append(task)
                tasksList.append(data)
        print(tasks)
        return tasksList

    else:
        print('Task Doesnot Exists')
        return {'message': "Task doesn't exist "}


async def add_Tasks(Tasks: taskModel):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database("ps2")
    collection = db.get_collection("appTask")
    row = await collection.find_one({"task": Tasks.task})

    print("Task doesn't Exist")
    Tsk = {
        '_id': None, 'task': Tasks.task, 'taskDescription': Tasks.taskDescription, 'username': Tasks.username,
        'technology': (Tasks.technology).lower(), 'workLink': Tasks.workLink
    }
    print(Tsk)
    dbTask = taskInDB(**Tsk)
    response = await collection.insert_one(dbTask.dict())
    return {'message': 'Task Added'}


async def delete_tasks(username: str, id: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("appTask")
    row = await collection.find_one({"_id": ObjectId(id)})
    if row:
        if row['username'] == username:
            print(row)
            await collection.delete_one(row)
            return {'message': 'Task Deleted'}
    else:
        return {'message': 'Task doesnot exists'}


async def Update_Tasks(username: str, id: str, task: str, taskDescription: str, workLink: str, technology: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database("ps2")
    collection = db.get_collection("appTask")
    row = await collection.find_one({'_id': ObjectId(id)})
    if row:
        if row['username'] == username:
            # raw = await collection.update_one({'_id': ObjectId(id)},
            # {'$set': {{'taskDescription': taskDescription}, {'task': task},{'workLink': workLink}, {'technology': technology}}})
            raw = await collection.update_one({'_id': ObjectId(id)}, {'$set': {'taskDescription': taskDescription}})
            raw = await collection.update_one({'_id': ObjectId(id)}, {'$set': {'task': task}})
            raw = await collection.update_one({'_id': ObjectId(id)}, {'$set': {'workLink': workLink}})
            raw = await collection.update_one({'_id': ObjectId(id)}, {'$set': {'technology': technology}})
            raw = await collection.update_one({'_id': ObjectId(id)},
                                              {'$set': {'updatedTime': datetime.datetime.utcnow()}})
            ram = taskInDB(**row)
            return {'message': 'Task Updated'}
        else:
            return {'message': 'Access Denied'}
    else:
        return {'message': 'Task doesnot exist'}


async def get_reportiesTask(username: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    TaskCollection = db.get_collection("appTasks")
    row = collection.find({"manager": username})
    allworks = []
    if row:
        async for user in row:
            task = await get_tasks_by_user(user['username'])
            allworks = allworks + task

    return allworks

async def getA_reportiesTask(username: str, reportieId: str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("users")
    TaskCollection = db.get_collection("appTask")
    row = await collection.find_one({"_id": ObjectId(reportieId)})
    tasks = TaskCollection.find({'username': row['username']})
    works: List[taskInDB] = []
    if row['manager'] == username:

        async for task in tasks:
            data = taskInDB(**task)
            works.append(data)

        return works