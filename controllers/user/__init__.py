from flask import render_template, Blueprint, request,redirect, flash, url_for
from models import engine, Usuarios, Horarios, Aluno, Professor, Cursos
from sqlalchemy.orm import Session
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from flask_login import login_required,current_user
from datetime import date


usuarios_bp = Blueprint('usuario',__name__, static_folder="static", template_folder="templates")


@usuarios_bp.route('/cadastro_usuario', methods = ['POST', 'GET'])
def cadastro_usuario():
    categoria = request.args.get('categoria')
    print(categoria)
    if categoria == 'aluno':
        return redirect(url_for('usuario.cadastro_aluno'))
    elif categoria == 'professor':
        return redirect(url_for('usuario.cadastro_professor'))
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
        

        # Verifica se o email já existe
        with Session(bind=engine) as session:
            usuario_existente = session.query(Usuarios).filter_by(matricula=matricula).first()
            if usuario_existente:
                flash("Matricula já cadastrada!", "error")
                return redirect(url_for('usuario.cadastro_usuario'))

            # Criptografa a senha
            senha_hash = generate_password_hash(senha)

            # Cria o usuário com todos os campos
            usuario = Aluno(
                matricula=matricula,
                nome=nome,
                senha=senha_hash,
                categoria='aluno',
                ano=ano,
                turno=turno,
                curso_id=curso
            )

            session.add(usuario)
            session.commit()

            flash("Usuário cadastrado com sucesso! Faça login.", "success")
            return redirect(url_for('auth.login'))

    with Session(bind=engine) as session:
         cursos = session.query(Cursos).all()
    return render_template('cadastro_aluno.html', cursos=cursos)


@usuarios_bp.route('/cadastro_professor', methods=['GET', 'POST'])
def cadastro_professor():
    if request.method == 'POST':
        matricula = int(request.form['matricula'])
        nome = request.form['nome']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            existe = session.query(Usuarios).filter_by(matricula=matricula).first()
            if existe:
                flash('Matrícula já cadastrada', 'error')
                return redirect(url_for('usuario.cadastro_professor'))
            senha_hash = generate_password_hash(senha)
            professor = Professor(matricula=matricula, nome=nome, senha=senha_hash, categoria='professor')
            session.add(professor)
            session.commit()
            flash('Professor cadastrado com sucesso', 'success')
            return redirect(url_for('auth.login'))

    return render_template('cadastro_professor.html')

@usuarios_bp.route('/dashboard')
@login_required
def dashboard():
    today = date.today().strftime("%Y-%m-%d")
    with Session(bind=engine) as session:
        if current_user.categoria == 'professor':
            total = (session.query(func.count(Horarios.id_horario)).filter(Horarios.id_professor == current_user.id_usuario).scalar())
            hoje = (session.query(func.count(Horarios.id_horario)).filter(Horarios.id_professor == current_user.id_usuario,Horarios.dias == today).scalar())
            proximo = (session.query(Horarios)
                       .filter(Horarios.id_professor == current_user.id_usuario, Horarios.dias >= today)
                       .order_by(Horarios.dias.asc(), Horarios.horario_inicio.asc())
                       .first())
        else:  # aluno
            total = (session.query(func.count(Horarios.id_horario)).join(Horarios.alunos).filter(Usuarios.id_usuario == current_user.id_usuario).scalar())
            hoje = (session.query(func.count(Horarios.id_horario)).join(Horarios.alunos).filter(Usuarios.id_usuario == current_user.id_usuario,Horarios.dias == today).scalar())
            proximo = (session.query(Horarios)
                       .join(Horarios.alunos)
                       .filter(Usuarios.id_usuario == current_user.id_usuario, Horarios.dias >= today)
                       .order_by(Horarios.dias.asc(), Horarios.horario_inicio.asc())
                       .first())
    return render_template('dashboard.html', nome=current_user.nome, hoje=hoje, total=total, proximo=proximo)



