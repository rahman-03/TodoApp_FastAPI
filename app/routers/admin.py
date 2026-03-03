from fastapi import APIRouter, HTTPException, Path, status
from typing import List

from app.schemas.user import UserResponse, AdminUserProfileUpdate
from app.models.user import Users
from app.auth.dependencies import admin_dependancy, db_dependancy

router = APIRouter(
    prefix = '/admin',
    tags=['admin']
)

# get all users
@router.get('/users', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def users_list(user : admin_dependancy, db: db_dependancy):
    return db.query(Users).all()

# get user by id
@router.get('/users/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user_detail(user : admin_dependancy, db: db_dependancy, user_id:int = Path(ge=1)):
    return db.query(Users).filter(Users.id ==user_id).first()

# delete user
@router.delete('/user/{user_id}',status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user : admin_dependancy, db: db_dependancy, user_id:int = Path(ge=1)):
    user_res = db.query(Users).filter(Users.id ==user_id).first()
    if not user_res:
        raise HTTPException(status_code=404,detail="Item not found")
    if user_res.id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Restricted to delete own account")
    db.delete(user_res)
    db.commit()

# update user
@router.put('/user_update/{user_id}',status_code=status.HTTP_200_OK)
async def user_update(user : admin_dependancy, db: db_dependancy, newdetails : AdminUserProfileUpdate, user_id:int = Path(ge=1)):
    user_res = db.query(Users).filter(Users.id == user_id).first()
    if not user_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if user_res.id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Restricted to delete own account")
    for field, value in newdetails.model_dump(exclude_unset=True).items():
        setattr(user_res, field, value)
    db.commit()
    db.refresh(user_res)
    return user_res