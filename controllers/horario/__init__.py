from flask import Blueprint, request, flash, render_template, redirect, url_for
from sqlalchemy.orm import Session, joinedload,selectinload
from sqlalchemy import text, select
from models import Horarios, Usuarios, engine, aluno_horario
from flask_login import current_user
from datetime import datetime, date

horarios_bp = Blueprint('horario',__name__, template_folder = 'templates', static_folder = 'static')


@horarios_bp.route('/cadastrar_horario', methods = ['POST','GET'])
def cadastrar_horario():
    if request.method == 'POST':
        dia = request.form['dia']
        horario_inicio = request.form['horario_inicio']
        horario_termino = request.form['horario_termino']
        sala = request.form['sala']
        
        dia = datetime.strptime(dia, "%Y-%m-%d").date()
        horario_inicio = datetime.strptime(horario_inicio, "%H:%M").time()
        horario_termino = datetime.strptime(horario_termino, "%H:%M").time()
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
    return render_template("cadastro_horario.html", today=date.today().isoformat())

@horarios_bp.route('/listar_horarios')
def listar_horarios():
    with Session(bind=engine) as session:
        horarios = (session.query(Horarios).options(joinedload(Horarios.professor)).all())
        
        horarios_inscritos_ids = []
        if current_user.is_authenticated and current_user.categoria == 'aluno':
            stmt = select(aluno_horario.c.id_horario).where(aluno_horario.c.id_aluno == int(current_user.get_id()))
            result = session.execute(stmt).scalars().all()
            horarios_inscritos_ids = list(result)
            
    return render_template("listar_horarios.html", horarios=horarios, horarios_inscritos_ids=horarios_inscritos_ids)


@horarios_bp.route('/listar_participar')
def listar_participar():
    with Session(bind=engine) as session:
        horarios = (
        session.query(Horarios)
        .options(
            selectinload(Horarios.professor),
            selectinload(Horarios.alunos)
        )).all()
    return render_template('horarios_participando.html', horarios=horarios)



@horarios_bp.route('/participar_ca' ,methods = ['POST','GET'])
def participar_ca():
    horario_id = request.form['horario_id']


    with Session(bind= engine) as sessao:
        horario = sessao.query(Horarios).filter_by(id_horario = horario_id).first()
        if current_user in horario.alunos:
            flash('você ja esta cadastrado nesse CA', 'error')
            return redirect(url_for('horario.listar_horarios'))
        
        horario.alunos.append(current_user)
        sessao.commit()
        sessao.close()
    return redirect(url_for('horario.listar_participar'))


@horarios_bp.route('/excluir_ca', methods = ['POST','GET'])
def excluir_ca():
    if request.method != 'POST':
        return redirect(url_for('horario.listar_horarios'))

    horario_id = request.form.get('horario_id')
    if not horario_id:
        flash('ID do horário não informado.', 'error')
        return redirect(url_for('horario.listar_horarios'))

    with Session(bind=engine) as sessao:
        try:
            horario = sessao.query(Horarios).filter_by(id_horario=horario_id).first()
            if not horario:
                flash('Horário não encontrado.', 'error')
                return redirect(url_for('horario.listar_horarios'))

            if current_user.categoria != 'professor' or current_user.id_usuario != horario.id_professor:
                flash('Você não tem permissão para excluir este horário.', 'error')
                return redirect(url_for('horario.listar_horarios'))
            sessao.execute(text('DELETE FROM horarios WHERE id_horario = :id'), { 'id': horario_id })
            sessao.commit()
            flash('Horário excluído com sucesso.', 'success')
        except Exception as e:
            flash(f"Erro de integridade {e}", 'error')
        finally:
            sessao.close()
    return redirect(url_for('horario.listar_horarios'))


@horarios_bp.route('/participantes/<int:horario_id>')
def listar_participantes(horario_id):
    with Session(bind=engine) as session:
        horario = session.query(Horarios).options(
            selectinload(Horarios.alunos)
        ).filter_by(id_horario=horario_id).first()
        
        if not horario:
            flash("Horário não encontrado.", "error")
            return redirect(url_for('horario.listar_horarios'))
            
        return render_template('listar_participantes.html', horario=horario)
