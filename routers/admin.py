from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal # type: ignore
from models import Todos, Users # type: ignore
from .auth import get_current_user # type: ignore


class UserResponse(BaseModel):
    id : int
    email : str
    username : str
    firstname : str
    lastname : str
    is_active : bool
    role : str
    phone_no : str | None

class AdminUserProfileUpdate(BaseModel):
    email : Optional[str] = None
    username : Optional[str] = None
    firstname : Optional[str] = None
    lastname : Optional[str] = None
    is_active : Optional[bool] = None
    role : Optional[str] = None
    phone_no : Optional[str] = None


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

# get all users
@router.get('/users', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def users_list(user : user_dependancy, db: db_dependancy):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    return db.query(Users).all()

# get user by id
@router.get('/users/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user_detail(user : user_dependancy, db: db_dependancy, user_id:int = Path(ge=1)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    return db.query(Users).filter(Users.id ==user_id).first()

# delete user
@router.delete('/user/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user : user_dependancy, db: db_dependancy, user_id:int = Path(ge=1)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    user_res = db.query(Users).filter(Users.id ==user_id).first()
    if not user_id:
        raise HTTPException(status_code=404,detail="Item not found")
    db.delete(user_res)
    db.commit()

# update user
@router.put('/user_update/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
async def user_update(user : user_dependancy, db: db_dependancy, newdetails : AdminUserProfileUpdate, user_id:int = Path(ge=1)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin access required')
    detail = db.query(Users).filter(Users.id == user_id).first()
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    for field, value in newdetails.model_dump(exclude_unset=True).items():
        setattr(detail, field, value)
    db.commit()
