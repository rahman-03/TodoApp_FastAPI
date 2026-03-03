from app.database import Base
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import relationship, Mapped,mapped_column

class Users(Base):
    __tablename__ = 'user'

    id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    email : Mapped[str] = mapped_column(String(255),unique=True)
    username : Mapped[str] = mapped_column(String(255),unique=True)
    firstname : Mapped[str] = mapped_column(String(255))
    lastname : Mapped[str] = mapped_column(String(255))
    hashed_pass : Mapped[str] = mapped_column(String(255))
    is_active : Mapped[bool] = mapped_column(Boolean,default=True)
    role : Mapped[str] = mapped_column(String(255), default="user")
    phone_no : Mapped[str] = mapped_column(String(255))

    todos = relationship(
        "Todos",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True
    )