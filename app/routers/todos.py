import json
from fastapi import APIRouter, HTTPException, Path, status

from app.schemas.todo import TodoRequest, TodoResponse, DeleteAllTodosRequest
from app.models.todo import Todos
from app.auth.hashing import authenticate
from app.auth.dependencies import db_dependancy, user_dependancy
from app.core.redis_client import redis_client


router = APIRouter(
    prefix = '/todos',
    tags=['todos']
)

# get all todos
@router.get('',response_model=list[TodoResponse] ,status_code=status.HTTP_200_OK)
async def root(user : user_dependancy, db: db_dependancy):
    cache_key = f"todos:{user.id}"
    cached = redis_client.get(cache_key)
    if cached:
        return [TodoResponse.model_validate_json(todo) for todo in json.loads(cached)]
    todos = db.query(Todos).filter(Todos.owner_id == user.id).all()
    redis_client.set(cache_key, json.dumps([TodoResponse.model_validate(todo).model_dump() for todo in todos]), ex=300)

    return todos

# get todo by id
@router.get('/{todo_id}',status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def todo_by_id(user : user_dependancy, db: db_dependancy, todo_id:int = Path(ge=1)):
    todo_res = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.id).first()
    if not todo_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo not found")
    return todo_res

# Create a todo
@router.post('', response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def todo_create(user : user_dependancy, db: db_dependancy, todo_req : TodoRequest):
    todo_data = todo_req.model_dump()
    todo_data["owner_id"] = user.id
    todo_model = Todos(**todo_data)
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    redis_client.delete(f"todos:{user.id}")
    return todo_model

# update a todo
@router.put('/{todo_id}', response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def todo_update(user : user_dependancy, db: db_dependancy,todo_req : TodoRequest, todo_id:int = Path(ge=1)):
    todo_model = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    for field, value in todo_req.model_dump(exclude_unset=True).items():
        setattr(todo_model, field, value)
    db.commit()
    db.refresh(todo_model)
    redis_client.delete(f"todos:{user.id}")
    return todo_model

# delete todo
@router.delete('/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def todo_delete(user : user_dependancy, db: db_dependancy, todo_id:int = Path(ge=1)):
    todo_res = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.id).first()
    if not todo_res:
        raise HTTPException(status_code=404,detail="Item not found")
    db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.id).delete()
    db.commit()
    redis_client.delete(f"todos:{user.id}")

# delete all todo
@router.delete("/deleteall", status_code=status.HTTP_200_OK)
async def delete_all_todos(user : user_dependancy, db: db_dependancy,request: DeleteAllTodosRequest):
    if not authenticate(user.username,request.password,db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid password")
    todos_query = db.query(Todos).filter(Todos.owner_id == user.id)
    count = todos_query.count()

    if count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No todos found")
    todos_query.delete(synchronize_session=False)
    db.commit()
    redis_client.delete(f"todos:{user.id}")

    return {
        "message": "All todos deleted successfully",
        "deleted_count": count
    }