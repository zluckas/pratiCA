from sqlalchemy.orm import DeclarativeBase,Session
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Time, ForeignKey
from datetime import time

from flask_login import UserMixin

import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('mysql+pymysql://root:29062007@localhost/db_pratica')

class Base(DeclarativeBase):
    pass

class Usuarios(Base,UserMixin):
    __tablename__ = 'usuarios'
    id_usuario:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email:Mapped[str] = mapped_column(String(50),unique=True)
    nome_usuario:Mapped[str] = mapped_column(String(50))
    senha:Mapped[str] = mapped_column(String(255))

    id_categoria:Mapped[int] = mapped_column(ForeignKey('categorias.id'))
    id_curso:Mapped[int] = mapped_column(ForeignKey('cursos.id')) 
    id_ano:Mapped[int] = mapped_column(ForeignKey('anos.id'))
    id_turno:Mapped[str] = mapped_column(ForeignKey('turnos.id'))
    
    categoria:Mapped['Categorias'] = relationship(back_populates='usuarios')
    curso:Mapped['Cursos'] = relationship(back_populates='usuarios')
    ano:Mapped['Anos'] = relationship(back_populates='usuarios')
    turno:Mapped['Turnos'] = relationship(back_populates='usuarios')

    horarios:Mapped[list['Horarios']] = relationship(back_populates='usuarios')

class Horarios(Base):
    __tablename__ = 'horarios'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dias:Mapped[str] = mapped_column(String(50), nullable=False) 
    horario_inicio:Mapped[time] = mapped_column(Time, nullable=False)
    horario_termino:Mapped[time] = mapped_column(Time, nullable=False)

    id_professor:Mapped[int] = mapped_column(ForeignKey('usuarios.id_usuario'))
    id_curso:Mapped[int] = mapped_column(ForeignKey('cursos.id'))
    id_turno:Mapped[int] = mapped_column(ForeignKey('turnos.id'))
    id_ano:Mapped[int] = mapped_column(ForeignKey('anos.id'))

    professor:Mapped['Usuarios'] = relationship(back_populates='horarios')
    curso:Mapped['Cursos'] = relationship(back_populates='horarios')
    turno:Mapped['Turnos'] = relationship(back_populates='horarios')
    ano:Mapped['Anos'] = relationship(back_populates='horarios')

class Cursos(Base):
    __tablename__ = 'cursos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(50), nullable=False)

    alunos:Mapped[list['Usuarios']] = relationship(back_populates='cursos')
    horarios:Mapped[list['Horarios']] = relationship(back_populates='cursos')

class Turnos(Base):
    __tablename__ = 'turnos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(50), nullable=False)

    alunos:Mapped[list['Usuarios']] = relationship(back_populates='turnos')
    horarios:Mapped[list['Horarios']] = relationship(back_populates='turnos')

class Anos(Base):
    __tablename__ = 'anos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(50), nullable=False)

    alunos:Mapped[list['Usuarios']] = relationship(back_populates='anos')
    horarios:Mapped[list['Horarios']] = relationship(back_populates='anos')

class Categorias(Base):
    __tablename__ = 'categorias'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(50), nullable=False)

    usuarios:Mapped[list['Usuarios']] = relationship(back_populates='categorias')
    horarios:Mapped[list['Usuarios']] = relationship(back_populates='categorias')


Base.metadata.create_all(bind=engine)