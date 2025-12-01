from flask import render_template, url_for, request, redirect,get_flashed_messages, flash, Blueprint
from sqlalchemy.orm import Session
from models import engine, Usuarios
from flask_login import login_user, logout_user
from werkzeug.security import  check_password_hash  

auth_bp = Blueprint('auth',__name__,static_folder="static", template_folder="templates")

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        with Session(bind=engine) as session:
            usuario = session.query(Usuarios).filter_by(matricula=matricula).first()
            if usuario and check_password_hash(usuario.senha, senha):
                login_user(usuario)
                return redirect(url_for('usuario.dashboard'))
            else:
                flash("Credenciais inválidas. Tente novamente.", "error")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))
