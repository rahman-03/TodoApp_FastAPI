from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256 # type: ignore




from database import SessionLocal # type: ignore
from models import Todos, Users # type: ignore
from .auth import get_current_user # type: ignore



router = APIRouter(
    prefix = '/user',
    tags=['user']
)

class DetailsChange(BaseModel):
    password : str
    email : Optional[str] = Field(description='Only if needed to change the value', default=None )
    username : Optional[str] = Field(description='Only if needed to change the value', default=None )
    firstname : Optional[str] = Field(description='Only if needed to change the value', default=None )
    lastname : Optional[str] = Field(description='Only if needed to change the value', default=None )
    # role : str = Field(description='Only if needed to change the value', default=None )
    phone_no : Optional[str] = Field(description='Only if needed to change the value', default=None )

class UserResponse(BaseModel):
    id : int
    email : str
    username : str
    firstname : str
    lastname : str
    role : str
    phone_no : str | None

class PassChange(BaseModel):
    old_pass : str
    new_pass : str
    conf_pass : str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session,Depends(get_db)]
user_dependancy = Annotated[dict , Depends(get_current_user)]


@router.get('/', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user : user_dependancy, db: db_dependancy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/change_pass',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user : user_dependancy, db: db_dependancy, newpass : PassChange):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    detail = db.query(Users).filter(Users.id == user.get('id')).first()
    if not pbkdf2_sha256.verify(newpass.old_pass, detail.hashed_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    if newpass.new_pass == newpass.conf_pass:
        detail.hashed_pass = pbkdf2_sha256.hash(newpass.new_pass)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password not matched')
    db.commit()


@router.put('/details_change',status_code=status.HTTP_204_NO_CONTENT)
async def details_change(user : user_dependancy, db: db_dependancy, newdetails : DetailsChange):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    detail = db.query(Users).filter(Users.id == user.get('id')).first()
    if not pbkdf2_sha256.verify(newdetails.password, detail.hashed_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    if newdetails.email:
        detail.email = newdetails.email
    if newdetails.username:
        detail.username = newdetails.username
    if newdetails.firstname:
        detail.firstname = newdetails.firstname
    if newdetails.lastname:
        detail.lastname = newdetails.lastname
    # if newdetails.role:
    #     detail.role = newdetails.role
    if newdetails.phone_no:
        detail.phone_no = newdetails.phone_no
    db.commit()