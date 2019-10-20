from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.helpers.auth import authenticated


mod = Blueprint('usuario', __name__)


# LISTADOS
@mod.route("/index/<rol>")
def index(rol):

    Usuario.db = get_db()
    usuarios = Usuario.get_usuarios_por_rol(rol)

    return render_template('usuarios/index.html', usuarios=usuarios)


# # prueba
# @app.route("/insertar")
# def insertar():
#     Usuario.db = get_db()
#     u = Usuario('mel@gmail.com', 'melisa', '0123', 'melisa', 'onofri')
#     ok = Usuario.insert(u)
#     if (ok):
#         return render_template('insertar.html', usuario = u)

