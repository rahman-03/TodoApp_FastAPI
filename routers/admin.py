from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal # type: ignore
from models import Todos # type: ignore
from .auth import get_current_user # type: ignore


class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3,max_length=100)
    priority : int  = Field(ge=1,le=5)
    complete : bool


router = APIRouter(
    prefix = '/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session , Depends(get_db)]
user_dependancy = Annotated[dict , Depends(get_current_user)]

# get all todos
@router.get('/')
async def root(user : user_dependancy, db: db_dependancy):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    return db.query(Todos).all()

# get todo by id
@router.get('/todo/{todo_id}',status_code=status.HTTP_200_OK)
async def todo_by_id(user : user_dependancy, db: db_dependancy, todo_id:int = Path(ge=1)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    todo_res = db.query(Todos).filter(Todos.id ==todo_id).first()
    if todo_res:
        return todo_res
    raise HTTPException(status_code=404,detail="Item not found")

# Create a todo
@router.post('/todo',status_code=status.HTTP_201_CREATED)
async def todo_create(user : user_dependancy, db: db_dependancy, todo_req : TodoRequest):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    todo_req = Todos(**todo_req.model_dump(), owner_id = user.get('id'))
    db.add(todo_req)
    db.commit()

# update a todo
@router.put('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def todo_update(user : user_dependancy, db: db_dependancy,todo_req : TodoRequest, todo_id:int = Path(ge=1)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id ==todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404,detail="Item not found")
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.priority = todo_req.priority
    todo_model.complete = todo_req.complete

    db.commit()

# delete todo
@router.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def todo_delete(user : user_dependancy, db: db_dependancy, todo_id:int = Path(ge=1)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    todo_res = db.query(Todos).filter(Todos.id ==todo_id).first()
    if not todo_res:
        raise HTTPException(status_code=404,detail="Item not found")
    db.query(Todos).filter(Todos.id ==todo_id).delete()
    db.commit()