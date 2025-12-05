from flask import Blueprint, request, flash, render_template, redirect, url_for
from sqlalchemy.orm import Session, joinedload
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
        horarios = (session.query(Horarios).options(joinedload(Horarios.professor)).all())
    return render_template("listar_horarios.html", horarios=horarios)


@horarios_bp.route('/listar_participar')
def listar_participar():
    with Session(bind=engine) as session:
        horarios = (session.query(Horarios).options(joinedload(Horarios.usuarios),joinedload(Horarios.professor) ).all())
    return render_template('horarios_participando.html', horarios = horarios)


@horarios_bp.route('/participar_ca' ,methods = ['POST','GET'])
def participar_ca():
    horario_id = request.form['horario_id']


    with Session(bind= engine) as sessao:
        horario = sessao.query(Horarios).filter_by(id_horario = horario_id).first()
        if current_user in horario.usuarios:
            flash('você ja esta cadastrado nesse CA', 'error')
            return redirect(url_for('listar_horarios'))
        
        horario.usuarios.append(current_user)
        sessao.commit()
        sessao.close()
    
