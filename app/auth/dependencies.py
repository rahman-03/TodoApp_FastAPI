from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt , JWTError, ExpiredSignatureError # type: ignore

from app.models.user import Users
from app.database import SessionLocal
from app.core.config import ACCESS_SECRET_KEY, ALGO

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session , Depends(get_db)]

async def get_current_user(token : Annotated[str , Depends(oauth2_bearer)], db: db_dependancy):
    try:
        payload = jwt.decode(token , ACCESS_SECRET_KEY , algorithms=ALGO)
        user = db.query(Users).filter(Users.id == payload.get('id')).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail = "Couldn\'t validate the user")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
user_dependancy = Annotated[Users , Depends(get_current_user)]

def admin_required(current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin access required")
    return current_user

admin_dependancy = Annotated[Users , Depends(admin_required)]
