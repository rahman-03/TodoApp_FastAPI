from fastapi import APIRouter, HTTPException, status
from passlib.hash import pbkdf2_sha256 # type: ignore
from app.core.redis_client import redis_client

from app.schemas.user import UserRequest, UserResponse, PassChange, DetailsChange
from app.auth.dependencies import db_dependancy, user_dependancy
from app.models.user import Users
from app.auth.hashing import authenticate

router = APIRouter(
    prefix = '/user',
    tags=['user']
)

@router.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependancy , new_user : UserRequest):
    if db.query(Users).filter(Users.email == new_user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(Users).filter(Users.username == new_user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    user_data = new_user.model_dump()
    user_data["hashed_pass"] = pbkdf2_sha256.hash(user_data.pop("password"))
    user_model = Users(**user_data)
    db.add(user_model)
    db.commit()
    return{
        "message": "User {username} Created",
    }


@router.get('', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user : user_dependancy, db: db_dependancy):
    cache_key = f"user:{user.id}"
    cached = redis_client.get(cache_key)
    if cached:
        return UserResponse.model_validate_json(cached)
    user_res = db.query(Users).filter(Users.id == user.id).first()
    if user_res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    redis_client.set(cache_key, UserResponse.model_validate(user_res).model_dump_json(), ex=300)
    return user_res


@router.put('/change_pass',status_code=status.HTTP_200_OK)
async def change_password(user : user_dependancy, db: db_dependancy, newpass : PassChange):
    user_res = db.query(Users).filter(Users.id == user.id).first()
    if not user_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')
    if not authenticate(user.username,newpass.old_pass,db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    if newpass.new_pass == newpass.conf_pass:
        user_res.hashed_pass = pbkdf2_sha256.hash(newpass.new_pass)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password not matched')
    db.commit()
    redis_client.delete(f"user:{user.id}")
    redis_client.delete("admin:users")
    return{
        "message": "Password Updated Successfully",
    }


@router.put('/details_change',status_code=status.HTTP_200_OK)
async def details_change(user : user_dependancy, db: db_dependancy, newdetails : DetailsChange):
    detail = db.query(Users).filter(Users.id == user.id).first()
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')
    if not authenticate(user.username,newdetails.password,db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    
    for field, value in newdetails.model_dump(exclude_unset=True).items():
        setattr(detail, field, value)
    db.commit()
    redis_client.delete(f"user:{user.id}")
    redis_client.delete("admin:users")
    return{
        "message": "Details Updated Successfully",
    }