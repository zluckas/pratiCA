from flask import render_template, Blueprint, request,redirect, flash, url_for
from models import engine, Usuarios, Cursos, Horarios
from sqlalchemy.orm import Session
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from flask_login import login_required,current_user
from datetime import date


usuarios_bp = Blueprint('usuario',__name__, static_folder="static", template_folder="templates")


@usuarios_bp.route('/cadastro_usuario', methods = ['POST', 'GET'])
def cadastro_usuario():
    if request.method == 'POST':
        matricula = int(request.form['matricula'])
        nome = request.form['nome']
        senha = request.form['senha']
        categoria = request.form['categoria']

        # Verifica se o email já existe
        with Session(bind=engine) as session:
            usuario_existente = session.query(Usuarios).filter_by(matricula=matricula).first()
            if usuario_existente:
                flash("Matricula já cadastrada!", "error")
                return redirect(url_for('usuario.cadastro_usuario'))

          
            senha_hash = generate_password_hash(senha)

            
            usuario = Usuarios(
                matricula=matricula,
                nome=nome,
                senha=senha_hash,
                categoria=categoria
            )

            session.add(usuario)
            session.commit()

            flash("Usuário cadastrado com sucesso! Faça login.", "sucesso")
            return redirect(url_for('auth.login'))

    return render_template('cadastro_usuario.html')

@usuarios_bp.route('/cadastro_aluno', methods = ['POST', 'GET'])
def cadastro_aluno():
    if request.method == 'POST':
        matricula = int(request.form['matricula'])
        nome = request.form['nome']
        senha = request.form['senha']
        curso = int(request.form['curso'])
        ano = request.form['ano']
        turno = request.form['turno']
        categoria = request.form['categoria']

        # Verifica se o email já existe
        with Session(bind=engine) as session:
            usuario_existente = session.query(Usuarios).filter_by(matricula=matricula).first()
            if usuario_existente:
                flash("Matricula já cadastrada!", "error")
                return redirect(url_for('usuario.cadastro_usuario'))

            # Criptografa a senha
            senha_hash = generate_password_hash(senha)

            # Cria o usuário com todos os campos
            usuario = Usuarios(
                matricula=matricula,
                nome=nome,
                senha=senha_hash,
                ano=ano,
                turno=turno,
                categoria=categoria,
                id_curso=curso
            )

            session.add(usuario)
            session.commit()

            flash("Usuário cadastrado com sucesso! Faça login.", "sucesso")
            return redirect(url_for('auth.login'))

    with Session(bind=engine) as session:
        cursos = session.query(Cursos).all()
    return render_template('cadastro_aluno.html', cursos=cursos)


@usuarios_bp.route('/cadastro_professor', methods = ['POST', 'GET'])
def cadastro_professor():   
   

    return render_template('cadastro_professor.html')
@usuarios_bp.route('/dashboard')
@login_required
def dashboard():
    with Session(bind=engine) as session:
        today = date.today().strftime("%Y-%m-%d")
        horarios_total = session.query(func.count(Horarios.id_professor)).filter_by(id_professor=current_user.id_usuario).scalar()
        horarios_hoje = session.query(func.count(Horarios.id_professor)).filter_by(id_professor=current_user.id_usuario, dias=today).scalar()
    return render_template('dashboard.html', nome=current_user.nome, hoje=horarios_hoje, total=horarios_total)



