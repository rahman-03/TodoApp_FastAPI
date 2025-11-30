import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.hash import pbkdf2_sha256 # type: ignore
from sqlalchemy.orm import Session
from jose import jwt , JWTError # type: ignore
from fastapi.templating import Jinja2Templates



from models import Users # type: ignore
from database import SessionLocal # type: ignore

SECRET_KEY = os.getenv("SECRET_KEY")
ALGO = os.getenv("ALGO")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


router = APIRouter(
    prefix = '/auth',
    tags=['auth']
)

class UserRequest(BaseModel):
    email : str
    username : str
    firstname : str
    lastname : str
    password : str
    role : str
    phone_no : str

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

templates = Jinja2Templates(directory='templates')

# Pages
@router.get('/login-page')
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {'request' : request})

@router.get('/register-page')
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {'request' : request})


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
        role = new_user.role,
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


def create_access_token(username : str, userid : int,role : str, expiry_delta : timedelta):
    encode = { 'sub' : username, 'id' : userid, 'role' : role }
    expires = datetime.now(timezone.utc) + expiry_delta
    encode.update({ 'exp' : expires })
    return jwt.encode(encode , SECRET_KEY , algorithm=ALGO)

async def get_current_user(token : Annotated[str , Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=ALGO)
        username = payload.get('sub')
        userid = payload.get('id')
        userrole = payload.get('role')
        if not username or not userid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail = "Couldn\'t validate the user")
        return { 'username' : username, 'id' : userid, 'role' : userrole }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail = "Couldn\'t validate the user")
    

@router.post('/token', response_model= Token)
async def auth_user(auth_form : Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependancy):
    user = authenticate(auth_form.username,auth_form.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail = "Couldn\'t validate the user")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token' : token , 'token_type' : 'bearer'}
