from sqlalchemy.orm import DeclarativeBase,Session
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String,Integer

from flask_login import UserMixin

engine = create_engine('sqlite:///banco.db')


class Base(DeclarativeBase):
    pass

class Usuario(Base,UserMixin):
    __tablename__ = 'usuarios'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email:Mapped[str] = mapped_column(String(50),unique=True)
    nome:Mapped[str] = mapped_column(String(50))
    senha:Mapped[str] = mapped_column(String(25))
    curso: Mapped[str] = mapped_column(String(50), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    turno: Mapped[str] = mapped_column(String(20), nullable=False)


Base.metadata.create_all(bind=engine)