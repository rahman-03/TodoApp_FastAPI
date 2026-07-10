from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from passlib.hash import pbkdf2_sha256 # type: ignore
import os
from dotenv import load_dotenv

from app.database import Base
from app.models.todo import Todos
from app.models.user import Users
from app.main import app

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    db = TestingSessionLocal()
    try:
        return db.query(Users).filter(
            Users.username == "testusername"
        ).first()
    finally:
        db.close()

def override_get_current_admin():
    db = TestingSessionLocal()
    try:
        return db.query(Users).filter(
            Users.username == "testuseradmin"
        ).first()
    finally:
        db.close()

client =TestClient(app)

@pytest.fixture
def insert_test_user():
    user = Users(
        email = 'test@samptest.com',
        username = 'testusername',
        firstname = 'testfirstname',
        lastname = 'testlastname',
        hashed_pass = pbkdf2_sha256.hash('testpassword'),
        is_active = True,
        role = 'user',
        phone_no = '1234567890'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user) 
    try:
        yield user
    finally:
        db.close()

@pytest.fixture
def insert_admin_user():
    user = Users(
        email = 'admin@samptest.com',
        username = 'testuseradmin',
        firstname = 'testadminfirstname',
        lastname = 'testadminlastname',
        hashed_pass = pbkdf2_sha256.hash('testadminpassword'),
        is_active = True,
        role = 'admin',
        phone_no = '1234569990'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user) 
    try:
        yield user
    finally:
        db.close()

@pytest.fixture
def insert_test_todo(insert_test_user):
    todo = Todos(
        title="EAT",
        description="breakfast",
        priority=5,
        complete=False,
        owner_id=insert_test_user.id
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    try:
        yield todo
    finally:
        db.close()

@pytest.fixture(autouse=True)
def cleanup_db():
    yield
    db = TestingSessionLocal()
    db.query(Todos).delete(synchronize_session=False)
    db.query(Users).delete(synchronize_session=False)
    db.commit()
    db.close()

