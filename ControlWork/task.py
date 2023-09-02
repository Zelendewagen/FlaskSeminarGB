import uvicorn
from fastapi import FastAPI

from ControlWork.database import database
from ControlWork.user_routes import router as user_router
from ControlWork.product_routes import router as product_routes
from ControlWork.order_routes import router as order_routes

app = FastAPI()
app.include_router(user_router)
app.include_router(product_routes)
app.include_router(order_routes)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("task:app", port=8001, reload=True)
