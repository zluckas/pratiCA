from flask import Blueprint, request

horarios_bp = Blueprint('horario',__name__, template_folder = 'templates', static_folder = 'static')


@horarios_bp.route('/cadastrar_horario')
def cadastrar_horario():
    if request.method == 'POST':
        dia = request.form['dia']
        horario_inicio = request.form['horario_inicio']
        horario_termino = request.form['horario_termino']
        sala = request.form['sala']
        