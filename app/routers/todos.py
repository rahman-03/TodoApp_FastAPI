from fastapi import APIRouter, HTTPException, Path, status

from app.schemas.todo import TodoRequest, DeleteAllTodosRequest
from app.models.todo import Todos
from app.auth.hashing import authenticate
from app.auth.dependencies import db_dependancy, user_dependancy


router = APIRouter(
    prefix = '/todos',
    tags=['todos']
)

# get all todos
@router.get('',status_code=status.HTTP_200_OK)
async def root(user : user_dependancy, db: db_dependancy):
    return db.query(Todos).filter(Todos.owner_id == user.id).all()

# get todo by id
@router.get('/{todo_id}',status_code=status.HTTP_200_OK)
async def todo_by_id(user : user_dependancy, db: db_dependancy, todo_id:int = Path(ge=1)):
    todo_res = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.id).first()
    if not todo_res:
        raise HTTPException(status_code=404,detail="Item not found")
    return todo_res

# Create a todo
@router.post('',status_code=status.HTTP_201_CREATED)
async def todo_create(user : user_dependancy, db: db_dependancy, todo_req : TodoRequest):
    todo_data = todo_req.model_dump()
    todo_data["owner_id"] = user.id
    user_model = Todos(**todo_data)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

# update a todo
@router.put('/{todo_id}',status_code=status.HTTP_200_OK)
async def todo_update(user : user_dependancy, db: db_dependancy,todo_req : TodoRequest, todo_id:int = Path(ge=1)):
    todo_model = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.id).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    for field, value in todo_req.model_dump(exclude_unset=True).items():
        setattr(todo_model, field, value)
    db.commit()
    db.refresh(todo_model)
    return todo_model

# delete todo
@router.delete('/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def todo_delete(user : user_dependancy, db: db_dependancy, todo_id:int = Path(ge=1)):
    todo_res = db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.id).first()
    if not todo_res:
        raise HTTPException(status_code=404,detail="Item not found")
    db.query(Todos).filter(Todos.id ==todo_id).filter(Todos.owner_id ==user.id).delete()
    db.commit()

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

    return {
        "message": "All todos deleted successfully",
        "deleted_count": count
    }