from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr
from passlib.hash import pbkdf2_sha256 # type: ignore
from sqlalchemy.orm import Session
from jose import jwt , JWTError, ExpiredSignatureError # type: ignore

from models import Users # type: ignore
from database import SessionLocal # type: ignore
from config import ACCESS_SECRET_KEY, REFREST_SECRET_KEY, ALGO

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


router = APIRouter(
    prefix = '/auth',
    tags=['auth']
)

class UserRequest(BaseModel):
    email: str
    username: str
    firstname: str
    lastname: str
    password: str
    phone_no: str


class Token(BaseModel):
    access_token : str
    token_type : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session,Depends(get_db)]


# Endpoints

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependancy , new_user : UserRequest):
    user_model = Users(
        email = new_user.email,
        username = new_user.username,
        firstname = new_user.firstname,
        lastname = new_user.lastname,
        hashed_pass = pbkdf2_sha256.hash(new_user.password),
        is_active = True,
        role = "user",
        phone_no = new_user.phone_no
    )

    db.add(user_model)
    db.commit()


def authenticate(username:str, password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        if pbkdf2_sha256.verify(password,user.hashed_pass):
            return user
    return False


def _create_jwt_token(data:dict, SECRET_KEY : str):
    encode = data.copy()
    return jwt.encode(encode , SECRET_KEY , algorithm=ALGO)

def create_access_token(username : str, userid : int,role : str):
    encode = { 'sub' : username, 
              'id' : userid, 
              'role' : role, 
              'type' : 'access'}
    expires = datetime.now(timezone.utc) + timedelta(minutes=20)
    encode.update({ 'exp' : expires })
    return _create_jwt_token(encode , ACCESS_SECRET_KEY)

def create_refresh_token(username : str, userid : int,role : str):
    encode = { 'sub' : username, 
              'id' : userid, 
              'role' : role, 
              'type' : 'refresh'}
    expires = datetime.now(timezone.utc) + timedelta(days=1)
    encode.update({ 'exp' : expires })
    return _create_jwt_token(encode , REFREST_SECRET_KEY)

async def get_current_user(token : Annotated[str , Depends(oauth2_bearer)], db: db_dependancy):
    try:
        payload = jwt.decode(token , ACCESS_SECRET_KEY , algorithms=ALGO)
        user = db.query(Users).filter(Users.id == payload.get('id')).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail = "Couldn\'t validate the user")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
        return { 'username' : payload.get('sub'), 'id' : payload.get('id'), 'role' : payload.get('role') }
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    
def admin_required(current_user: Users = Depends(get_current_user)):
    if current_user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin access required")
    return current_user
    

@router.post('/token', response_model= Token)
async def auth_user(auth_form : Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependancy,response : Response):
    user = authenticate(auth_form.username,auth_form.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail = "Couldn\'t validate the user")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    access_token = create_access_token(user.username, user.id, user.role)
    refresh_token = create_refresh_token(user.username, user.id, user.role)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="None",
        max_age=60 * 60 * 24,
        path="/"
    )
    return {'access_token' : access_token , 'token_type' : 'bearer'}

@router.post("/refresh", response_model= Token)
async def refresh_token(request : Request):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        payload = jwt.decode(refresh_token, REFREST_SECRET_KEY, algorithms=ALGO)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        new_access_token = create_access_token(payload.get("sub"),payload.get("id"),payload.get("role"))
        return {"access_token": new_access_token, 'token_type' : 'bearer'}
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="None",
        path="/"
    )
    return {"message": "Logged out"}