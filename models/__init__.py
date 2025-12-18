from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Time, ForeignKey, Integer
from datetime import time
from sqlalchemy.orm import Session


from flask_login import UserMixin

import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('sqlite:///pratica.db', echo=False)


class Base(DeclarativeBase):
    pass


aluno_horario = Table(
    'aluno_horario',
    Base.metadata,
    Column('id_aluno', ForeignKey('alunos.id_usuario'), primary_key=True),
    Column('id_horario', ForeignKey('horarios.id_horario'), primary_key=True)
)


class Usuarios(Base, UserMixin):
    __tablename__ = 'usuarios'

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    matricula: Mapped[int] = mapped_column(Integer, unique=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": categoria,
        "polymorphic_identity": "usuario",
    }

    def get_id(self):
        return str(self.id_usuario)

class Professor(Usuarios):
    __tablename__ = 'professores'

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey('usuarios.id_usuario'),
        primary_key=True
    )

    horarios_ministrados: Mapped[list['Horarios']] = relationship(
        'Horarios',
        back_populates='professor'
    )

    __mapper_args__ = {
        "polymorphic_identity": "professor",
    }


class Aluno(Usuarios):
    __tablename__ = 'alunos'

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey('usuarios.id_usuario'),
        primary_key=True
    )

    ano: Mapped[str] = mapped_column(String(20), nullable=False)
    turno: Mapped[str] = mapped_column(String(20), nullable=False)

    curso_id: Mapped[int] = mapped_column(
        ForeignKey('cursos.id'),
        nullable=False
    )

    curso: Mapped['Cursos'] = relationship(
        back_populates='alunos'
    )

    horarios: Mapped[list['Horarios']] = relationship(
        'Horarios',
        secondary=aluno_horario,
        back_populates='alunos'
    )

    __mapper_args__ = {
        "polymorphic_identity": "aluno",
    }


class Horarios(Base):
    __tablename__ = 'horarios'

    id_horario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id_professor: Mapped[int] = mapped_column(
        ForeignKey('professores.id_usuario'),
        nullable=False
    )

    dias: Mapped[str] = mapped_column(String(50), nullable=False)
    horario_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    horario_termino: Mapped[time] = mapped_column(Time, nullable=False)
    sala: Mapped[str] = mapped_column(String(50), nullable=False)

    professor: Mapped['Professor'] = relationship(
        'Professor',
        back_populates='horarios_ministrados'
    )

    alunos: Mapped[list['Aluno']] = relationship(
        'Aluno',
        secondary=aluno_horario,
        back_populates='horarios'
    )
    
    
class Cursos(Base):     
    __tablename__ = 'cursos'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    alunos: Mapped[list['Aluno']] = relationship(back_populates='curso',cascade='all, delete-orphan')

    @staticmethod
    def seed_database(session):
    # Verifica se já existem dados para não duplicar
        if not session.query(Cursos).first():
            cursos = [
                Cursos(nome="Informática"),
                Cursos(nome="Eletrotécnica"),
                Cursos(nome="Têxtil"),
                Cursos(nome="Vestuário")
            ]
            session.add_all(cursos)
            session.commit()
            print("Tabela de cursos populada com sucesso!")


