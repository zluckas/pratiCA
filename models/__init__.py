from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Time, ForeignKey, Integer
from datetime import time

from flask_login import UserMixin

import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('mysql+pymysql://root:@localhost/db_pratica')

class Base(DeclarativeBase):
    pass

usuario_horario = Table(
    'usuario_horario', 
    Base.metadata,
    Column('id_usuario', ForeignKey('usuarios.id_usuario'), primary_key=True),
    Column('id_horario', ForeignKey('horarios.id_horario'), primary_key=True)
)

class Usuarios(Base, UserMixin):
    __tablename__ = 'usuarios'
    id_usuario:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    matricula:Mapped[int] = mapped_column(Integer, unique=True)
    nome:Mapped[str] = mapped_column(String(50))
    senha:Mapped[str] = mapped_column(String(255))
    ano:Mapped[str] = mapped_column(String(20), nullable=False)
    turno:Mapped[str] = mapped_column(String(20), nullable=False)
    categoria:Mapped[str] = mapped_column(String(20), nullable=False)
    id_curso:Mapped[int] = mapped_column(ForeignKey('cursos.id')) 
    
    curso:Mapped['Cursos'] = relationship(back_populates='usuarios')

    horarios:Mapped[list['Horarios']] = relationship(secondary=usuario_horario, back_populates='usuarios')

    def get_id(self):
        return str(self.id_usuario)


class Horarios(Base):
    __tablename__ = 'horarios'
    id_horario:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dias:Mapped[str] = mapped_column(String(50), nullable=False) 
    horario_inicio:Mapped[time] = mapped_column(Time, nullable=False)
    horario_termino:Mapped[time] = mapped_column(Time, nullable=False)
    sala:Mapped[str] = mapped_column(String(50), nullable=False)

    usuarios:Mapped[list['Usuarios']] = relationship(secondary=usuario_horario, back_populates='horarios')
    
class Cursos(Base):
    __tablename__ = 'cursos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(50), nullable=False)

    usuarios:Mapped[list['Usuarios']] = relationship(back_populates='curso')


Base.metadata.create_all(bind=engine)