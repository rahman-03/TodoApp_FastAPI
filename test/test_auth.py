from fastapi import status
from jose import jwt # type: ignore
import pytest
from fastapi import HTTPException

from app.auth.dependencies import get_db, get_current_user
from app.auth.hashing import authenticate
from app.auth.jwt import create_access_token
from app.core.config import ACCESS_SECRET_KEY, ALGO
from .utils import *

app.dependency_overrides[get_db] = override_get_db

# test authenticate user
def test_authenticate_user(insert_test_user):
    db = TestingSessionLocal()
    try:
        auth_user = authenticate(insert_test_user.username, 'testpassword', db)
        assert auth_user is not None

        non_auth_user = authenticate('abc', 'testpassword', db)
        assert non_auth_user is False

        wrong_pass = authenticate(insert_test_user.username, 'password', db)
        assert wrong_pass is False
    finally:
        db.close()

# test create_access_token
def test_create_access_token(insert_test_user):
    token = create_access_token(insert_test_user.username, insert_test_user.id, insert_test_user.role)
    decode_token = jwt.decode(token , ACCESS_SECRET_KEY , algorithms=ALGO)

    assert decode_token['sub'] == insert_test_user.username
    assert decode_token['id'] == insert_test_user.id
    assert decode_token['role'] == insert_test_user.role
    
# test get_current_user valid user
@pytest.mark.asyncio
async def test_get_current_user_valid_user(insert_test_user):
    db = TestingSessionLocal()
    try:
        encode = {'sub' : 'testusername', 'id' : insert_test_user.id, 'role' : 'admin'}
        token = jwt.encode(encode, ACCESS_SECRET_KEY, algorithm=ALGO)

        user = await get_current_user(token=token,db=db)
        assert user.username == 'testusername'
        assert user.id == insert_test_user.id
        assert user.role == 'user'
    finally:
        db.close()

# test get_current_user missing payload
@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    db = TestingSessionLocal()
    try:
        encode = {'role' : 'admin'}
        token = jwt.encode(encode, ACCESS_SECRET_KEY, algorithm=ALGO)
        with pytest.raises(HTTPException) as excpinfo:
            await get_current_user(token=token,db=db)

        assert excpinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert excpinfo.value.detail == "Couldn\'t validate the user"
    finally:
        db.close()