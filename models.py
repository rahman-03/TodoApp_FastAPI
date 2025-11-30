from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class Users(Base):
    __tablename__ = 'user'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(255),unique=True)
    username = Column(String(255),unique=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    hashed_pass = Column(String(255))
    is_active = Column(String(255),default=True)
    role = Column(String(255))
    phone_no = Column(String(255))



class Todos(Base):
    __tablename__ = 'todo'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(255))
    description = Column(String(500))
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer,ForeignKey("user.id"))
