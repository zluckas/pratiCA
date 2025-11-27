from flask import render_template, Blueprint, request,redirect, flash, url_for
from models import engine, Usuarios, Turnos, Anos, Cursos
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from flask_login import login_required,current_user


usuarios_bp = Blueprint('usuario',__name__, static_folder="static", template_folder="templates")


@usuarios_bp.route('/cadastro', methods = ['POST', 'GET'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        curso = request.form['curso']
        ano = request.form['ano']
        turno = request.form['turno']

        # Verifica se o email já existe
        with Session(bind=engine) as session:
            usuario_existente = session.query(Usuarios).filter_by(email=email).first()
            if usuario_existente:
                flash("E-mail já cadastrado! Escolha outro.", "error")
                return redirect(url_for('usuario.cadastro_usuario'))

            # Criptografa a senha
            senha_hash = generate_password_hash(senha)

            # Cria o usuário com todos os campos
            usuario = Usuarios(
                nome=nome,
                email=email,
                senha=senha_hash,
                curso=curso,
                ano=ano,
                turno=turno
            )

            session.add(usuario)
            session.commit()

            flash("Usuário cadastrado com sucesso! Faça login.", "sucesso")
            return redirect(url_for('auth.login'))

    with Session(bind=engine) as session:
        cursos = session.query(Cursos).all()
        anos = session.query(Anos).all()
        turnos = session.query(Turnos).all()
    return render_template('cadastro_usuario.html', cursos=cursos, anos=anos, turnos=turnos)


@usuarios_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome=current_user.nome)