from flaskps import app
from flask import render_template, url_for, flash, request
from flaskps.db import get_db
from flaskps.models.Usuario import Usuario



def index():
    Usuario.db = get_db()
    usuarios = Usuario.get_usuarios_por_rol(4)

    return render_template('usuarios/index.html', usuarios=usuarios)