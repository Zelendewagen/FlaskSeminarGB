# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
#
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

TASKS = []


class Task(BaseModel):
    id_: int
    title: str
    description: str
    status: str


@app.get('/tasks/')
async def all_tasks():
    return {'tasks': TASKS}


@app.post('/task/add')
async def add_task(task: Task):
    TASKS.append(task)
    return {"task": task, "status": "added"}


@app.put('/task/update/{task_id}')
async def update_task(task_id: int, task: Task):
    for t in TASKS:
        if t.id_ == task_id:
            t.title = task.title
            t.description = task.description
            t.status = task.status
            return {"task": task, "status": "updated"}
    return HTTPException(404, 'Task not found')


@app.delete('/task/delete/{task_id}')
async def delete_task(task_id: int):
    for t in TASKS:
        if t.id_ == task_id:
            TASKS.remove(t)
            return {"status": "success"}
    return HTTPException(404, 'Task not found')
