from passlib.hash import pbkdf2_sha256 # type: ignore
from app.models.user import Users # type: ignore

def authenticate(username:str, password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        if pbkdf2_sha256.verify(password,user.hashed_pass):
            return user
    return False