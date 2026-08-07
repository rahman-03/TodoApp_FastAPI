import json
from fastapi import APIRouter, HTTPException, Path, status
from app.core.redis_client import redis_client

from app.schemas.user import UserResponse, AdminUserProfileUpdate
from app.models.user import Users
from app.auth.dependencies import admin_dependancy, db_dependancy

router = APIRouter(
    prefix = '/admin',
    tags=['admin']
)

# get all users
@router.get('/users', response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def users_list(user : admin_dependancy, db: db_dependancy):
    cache_key = "admin:users"
    cached = redis_client.get(cache_key)
    if cached:
        return [UserResponse.model_validate_json(user) for user in json.loads(cached)]
    users_res = db.query(Users).all()
    redis_client.set(cache_key, json.dumps([UserResponse.model_validate(user).model_dump() for user in users_res]), ex=300)
    
    return users_res

# get user by id
@router.get('/user/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user_detail(user : admin_dependancy, db: db_dependancy, user_id:int = Path(ge=1)):
    cache_key = f"user:{user_id}"
    cached = redis_client.get(cache_key)
    if cached:
        return UserResponse.model_validate_json(cached)
    user_res = db.query(Users).filter(Users.id == user_id).first()
    if user_res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    redis_client.set(cache_key, UserResponse.model_validate(user_res).model_dump_json(), ex=300)
    return user_res

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
    redis_client.delete(f"user:{user_id}")
    redis_client.delete("admin:users")

# update user
@router.put('/user_update/{user_id}',status_code=status.HTTP_200_OK)
async def user_update(user : admin_dependancy, db: db_dependancy, newdetails : AdminUserProfileUpdate, user_id:int = Path(ge=1)):
    user_res = db.query(Users).filter(Users.id == user_id).first()
    if not user_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if user_res.id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Restricted to Update own account")
    for field, value in newdetails.model_dump(exclude_unset=True).items():
        setattr(user_res, field, value)
    db.commit()
    db.refresh(user_res)
    redis_client.delete(f"user:{user_id}")
    redis_client.delete("admin:users")
    return user_res