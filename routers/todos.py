from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal # type: ignore
from models import Todos # type: ignore
from .auth import authenticate, get_current_user # type: ignore


class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3,max_length=100)
    priority : int  = Field(ge=1,le=5)
    complete : bool


router = APIRouter(
    prefix = '/todos',
    tags=['todos']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session , Depends(get_db)]
user_dependancy = Annotated[dict , Depends(get_current_user)]


# Endpoints
# get all todos
@router.get('/')
async def root(user : user_dependancy, db: db_dependancy):
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

# get todo by id
@router.get('/todo/{todo_id}',status_code=status.HTTP_200_OK)
async def todo_by_id(user : user_dependancy, db: db_dependancy, todo_id:int = Path(ge=1)):
    todo_res = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.get('id')).first()
    if todo_res:
        return todo_res
    raise HTTPException(status_code=404,detail="Item not found")

# Create a todo
@router.post('/todo',status_code=status.HTTP_201_CREATED)
async def todo_create(user : user_dependancy, db: db_dependancy, todo_req : TodoRequest):
    todo_req = Todos(**todo_req.model_dump(), owner_id = user.get('id'))
    db.add(todo_req)
    db.commit()
    return {
        "message": "todo created successfully"
    }

# update a todo
@router.put('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def todo_update(user : user_dependancy, db: db_dependancy,todo_req : TodoRequest, todo_id:int = Path(ge=1)):
    todo_model = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.get('id')).first()
    if not todo_model:
        raise HTTPException(status_code=404,detail="Item not found")
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.priority = todo_req.priority
    todo_model.complete = todo_req.complete

    db.commit()
    return {
        "message": "todo {todo_id} updated successfully"
    }

# delete todo
@router.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def todo_delete(user : user_dependancy, db: db_dependancy, todo_id:int = Path(ge=1)):
    todo_res = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.get('id')).first()
    if not todo_res:
        raise HTTPException(status_code=404,detail="Item not found")
    db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.get('id')).delete()
    db.commit()
    return {
        "message": "todo {todo_id} deleted successfully"
    }


class DeleteAllTodosRequest(BaseModel):
    password: str

# delete all todo
@router.delete("/deleteall", status_code=status.HTTP_200_OK)
async def delete_all_todos(user : user_dependancy, db: db_dependancy,request: DeleteAllTodosRequest):
    if not authenticate(user.get('username'),request.password,db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password"
        )

    todos_query = db.query(Todos).filter(
        Todos.owner_id == user.get("id")
    )

    count = todos_query.count()

    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No todos found"
        )

    todos_query.delete(synchronize_session=False)
    db.commit()

    return {
        "message": "All todos deleted successfully",
        "deleted_count": count
    }