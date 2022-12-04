from fastapi import FastAPI, HTTPException
from database import (fetch_all_todos,create_todo, update_todo, remove_todo,fetch_one_todo)
from fastapi.middleware.cors import CORSMiddleware
from model import Todo


# App object 
app = FastAPI()

origins = ['mongodb://localhost:27017']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"ping":"pong"}


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("api/todo{title}",response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)

    if response:
        return response
    raise HTTPException(404, f"There is no TODO item with this title {title}")


@app.post("/api/todo", response_model=Todo)
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response : 
        return response
    raise HTTPException(400, "Something went wrong / Bad request")

@app.put("/api/todo{title}/",response_model=Todo)
async def put_todo(title:str, desc:str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404,f"There is no TODO item with this title {title}")

@app.delete("/api/todo{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Succesfully deleted todo item ! "
    raise HTTPException(404, f"There is no Todo Item this title {title}")

