
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schema import Todo

app = FastAPI()

#import services
from database import(
    fetch_one_todo,
    fetch_all_todo,
    create_todo,
    update_todo,
    remove_todo
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Fetch all todo
@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todo()
    return response

#Fetch specific todo
@app.get("/api/todo/{title}", response_model = Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no TODO on {title}")

#Save a todo
@app.post("/api/todo/save", response_model = Todo)
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

#Update todo
@app.put("/api/todo/update/{title}", response_model = Todo)
async def put_todo(title : str, todo:Todo):
    response = await update_todo(title,todo.description)
    if response:
        return response
    raise HTTPException(404, f"there is no title {title}")
    

#Delete todo
@app.delete("/api/todo/delete/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted"
    raise HTTPException(404, "Not found")
    

