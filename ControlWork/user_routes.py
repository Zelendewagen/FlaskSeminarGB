from typing import List, Dict
from fastapi import APIRouter
from starlette.responses import JSONResponse

from ControlWork.database import users_table, database
from ControlWork.models import User, UserIn

router = APIRouter()


async def check_user(user_id: int):
    query = users_table.select().where(users_table.c.id == user_id)
    return await database.fetch_one(query)


@router.get('/get_all_users/', response_model=List[User], tags=["users"])
async def get_all_users():
    query = users_table.select()
    return await database.fetch_all(query)


@router.get('/get_user/{user_id}', response_model=User | Dict, tags=["users"])
async def get_user(user_id: int):
    query = users_table.select().where(users_table.c.id == user_id)
    result = await database.fetch_one(query)
    if result:
        return result
    return JSONResponse(status_code=404, content={'error': 'User Not Found'})


@router.post('/add_user/', response_model=User, tags=["users"])
async def add_user(user: UserIn):
    query = users_table.insert().values(**user.model_dump())
    password = user.password.get_secret_value()
    query = query.values(password=password)
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@router.put('/update_user/{user_id}', response_model=User, tags=["users"])
async def update_user(new_user: UserIn, user_id: int):
    if not check_user(user_id):
        return JSONResponse(status_code=404, content={'error': 'User Not Found'})
    query = users_table.update().where(users_table.c.id == user_id).values(**new_user.model_dump())
    password = new_user.password.get_secret_value()
    query = query.values(password=password)
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@router.delete('/delete_user/{user_id}', tags=["users"])
async def delete_user(user_id: int):
    if not check_user(user_id):
        return JSONResponse(status_code=404, content={'error': 'User Not Found'})
    query = users_table.delete().where(users_table.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted"}
