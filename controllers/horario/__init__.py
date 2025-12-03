from flask import Blueprint, request, flash, render_template, redirect, url_for
from sqlalchemy.orm import Session
from models import Horarios, Usuarios, engine
from flask_login import current_user

horarios_bp = Blueprint('horario',__name__, template_folder = 'templates', static_folder = 'static')


@horarios_bp.route('/cadastrar_horario', methods = ['POST','GET'])
def cadastrar_horario():
    if request.method == 'POST':
        dia = request.form['dia']
        horario_inicio = request.form['horario_inicio']
        horario_termino = request.form['horario_termino']
        sala = request.form['sala']

        with Session(bind=engine) as session:
            usuario = session.query(Usuarios).filter_by(id_usuario=current_user.id_usuario).first()
            if usuario.categoria != 'professor':
                flash("Apenas professores podem cadastrar horários.", 'error')

            else:
                novo_horario = Horarios(
                    dias=dia,
                    horario_inicio=horario_inicio,
                    horario_termino=horario_termino,
                    sala=sala,
                    id_professor = current_user.id_usuario)
                session.add(novo_horario)  
                session.commit()
                flash("Horário cadastrado com sucesso!", "success")
    
                return redirect(url_for('horario.listar_horarios'))
    return render_template("cadastro_horario.html")

@horarios_bp.route('/listar_horarios')
def listar_horarios():
    with Session(bind=engine) as session:
        horarios = session.query(Horarios).all()
    return render_template("listar_horarios.html", horarios=horarios)

