from flask import Flask, render_template, url_for, request, redirect,get_flashed_messages, flash
from sqlalchemy.orm import Session
from models import engine, Usuario
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'senha_super_secreta1234567'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as session:
        return session.get(Usuario, int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastro_usuario', methods=['GET', 'POST'])
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
            usuario_existente = session.query(Usuario).filter_by(email=email).first()
            if usuario_existente:
                flash("E-mail já cadastrado! Escolha outro.", "erro")
                return redirect(url_for('cadastro_usuario'))

            # Criptografa a senha
            senha_hash = generate_password_hash(senha)

            # Cria o usuário com todos os campos
            usuario = Usuario(
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
            return redirect(url_for('login'))

    return render_template('cadastro_usuario.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            usuario = session.query(Usuario).filter_by(email=email).first()
            if usuario and check_password_hash(usuario.senha, senha):
                login_user(usuario)
                return redirect(url_for('dashboard'))
            else:
                flash("Credenciais inválidas. Tente novamente.", "erro")

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome=current_user.nome)