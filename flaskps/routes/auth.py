from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Configuracion import Configuracion
from flaskps.forms import LoginForm
from flaskps.helpers.auth import authenticated


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
            print(len(user))

            if not user:
                flash("Usuario o clave incorrecto.")
                error=1
                return render_template("login.html", title='Iniciar Sesión', form=form, error=error)

            # crear la sesion, datos del usuario
            session['user'] = user[0]
            
            # crear lista con todos los permisos del usuario, contemplando mas de un rol
            permisos = []
            for tupla in user:
                tupla_permisos = Usuario.get_permisos(tupla['id_rol'])
                for p in tupla_permisos:
                    permisos.append(p['nombre'])

            # eliminar permisos repetidos
            permisos = set(permisos)    

            # cargar lista de permisos del usuario
            session['permisos'] = permisos

            Configuracion.db = get_db()
            config = Configuracion.get_config()
            return render_template("home.html", config=config)
        else:
            flash("Debe completar todos los campos")
            error=1
    return render_template("login.html", title='Iniciar Sesión', form=form, error=error)


@mod.route("/logout")
def logout():
    if not authenticated(session):
        return redirect("/login")
    
    # eliminar sesion
    del session['user']
    del session['permisos']
    session.clear()
    flash("La sesión se cerró correctamente.")

    Configuracion.db = get_db()
    config = Configuracion.get_config()
    return render_template("home.html", config=config)