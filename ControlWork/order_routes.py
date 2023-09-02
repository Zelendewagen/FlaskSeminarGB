from typing import List, Dict
from fastapi import APIRouter
from starlette.responses import JSONResponse

from ControlWork.database import orders_table, database
from ControlWork.models import Order, OrderIn

router = APIRouter()


async def check_order(order_id: int):
    query = orders_table.select().where(orders_table.c.id == order_id)
    return await database.fetch_one(query)


@router.get('/get_all_orders/', response_model=List[Order], tags=["orders"])
async def get_all_orders():
    query = orders_table.select()
    return await database.fetch_all(query)


@router.get('/get_order/{order_id}', response_model=Order | Dict, tags=["orders"])
async def get_order(order_id: int):
    query = orders_table.select().where(orders_table.c.id == order_id)
    result = await database.fetch_one(query)
    if result:
        return result
    return JSONResponse(status_code=404, content={'error': 'Order Not Found'})


@router.post('/add_order/', response_model=Order, tags=["orders"])
async def add_order(order: Order):
    query = orders_table.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@router.put('/update_order/{order_id}', response_model=Order, tags=["orders"])
async def update_order(new_order: OrderIn, order_id: int):
    if not check_order(order_id):
        return JSONResponse(status_code=404, content={'error': 'Order Not Found'})
    query = orders_table.update().where(orders_table.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@router.delete('/delete_order/{order_id}', tags=["orders"])
async def delete_order(order_id: int):
    if not check_order(order_id):
        return JSONResponse(status_code=404, content={'error': 'Order Not Found'})
    query = orders_table.delete().where(orders_table.c.id == order_id)
    await database.execute(query)
    return {"message": "Product deleted"}