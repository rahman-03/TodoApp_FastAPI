from datetime import datetime, timedelta, timezone
from jose import jwt # type: ignore
from app.core.config import ACCESS_SECRET_KEY, REFRESH_SECRET_KEY, ALGO

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
    return _create_jwt_token(encode , REFRESH_SECRET_KEY)