from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Configuracion import Configuracion
from flaskps.forms import LoginForm
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible 


mod = Blueprint('auth', __name__)


# AUTH
@mod.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = 0
    
    if request.method == 'POST':
       
        if form.validate_on_submit():
            Usuario.db = get_db()
            
            user = Usuario.find_by_email_and_pass(form.email.data, form.password.data)
            
            if not user:
                flash("Usuario o clave incorrecto.")
                error=1
                return render_template("login.html", title='Iniciar Sesión', form=form, error=error)
            
            # crear la sesion, datos del usuario
            session['user'] = user[0]
            # cargar los roles del usuario
            session['roles'] = get_roles(user[0]['id'])
            # cargar lista de permisos del usuario
            session['permisos'] = get_permisos(user)
            
            session.permanent = True

            return redirect("/home")
        else:
            flash("Debe completar todos los campos")
            error=1
    return render_template("login.html", title='Iniciar Sesión', form=form, error=error)


@mod.route("/logout")
def logout():
    if not authenticated(session):
        return redirect("/login")
    else:
        # eliminar sesion
        del session['user']
        del session['roles']
        del session['permisos']
        session.clear()
        

    if not sitio_disponible():
        return render_template("mantenimiento.html")
    flash("La sesión se cerró correctamente.")
    return redirect("/home")



# OPERACIONES

def get_permisos(user):
    # crear lista con todos los permisos del usuario, contemplando mas de un rol
    permisos = []
    for tupla in user:
        tupla_permisos = Usuario.get_permisos(tupla['id_rol'])
        for p in tupla_permisos:
            permisos.append(p['nombre'])
    # eliminar permisos repetidos
    return set(permisos)

def get_roles(id):
    tabla_roles = Usuario.get_roles(id)
    roles = []
    for tupla in tabla_roles:
        roles.append(tupla['nombre'])
    return roles