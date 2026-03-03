from app.database import Base
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped,mapped_column

class Todos(Base):
    __tablename__ = 'todo'

    id : Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    title : Mapped[str] = mapped_column(String(255))
    description : Mapped[str] = mapped_column(String(500))
    priority : Mapped[int] = mapped_column(Integer)
    complete : Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id : Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    owner = relationship("Users", back_populates="todos")