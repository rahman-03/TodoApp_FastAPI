from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt , JWTError, ExpiredSignatureError # type: ignore

from app.auth.dependencies import db_dependancy, oauth2_bearer
from app.auth.hashing import authenticate
from app.auth.jwt import create_access_token, create_refresh_token
from app.core.config import REFRESH_SECRET_KEY, ALGO

router = APIRouter(
    prefix = '/auth',
    tags=['auth']
)

class Token(BaseModel):
    access_token : str
    token_type : str
    
@router.post('/login', response_model= Token)
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
        samesite="none",
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
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=ALGO)
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
        samesite="none",
        path="/"
    )
    return {"message": "Logged out"}