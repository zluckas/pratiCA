from flask import Flask
from sqlalchemy.orm import Session
from models import engine, Usuarios
from flask_login import LoginManager
from controllers import auth, user, horario


app = Flask(__name__)
app.config['SECRET_KEY'] = 'senha_super_secreta1234567'

app.register_blueprint(user.usuarios_bp)
app.register_blueprint(auth.auth_bp)
app.register_blueprint(horario.horarios_bp)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as session:
        return session.get(Usuarios, int(user_id))

