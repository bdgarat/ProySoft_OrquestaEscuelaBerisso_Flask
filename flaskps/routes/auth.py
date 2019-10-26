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

    if form.validate_on_submit():
        Usuario.db = get_db()
        
        user = Usuario.find_by_email_and_pass(form.email.data, form.password.data)
        
        if not user:
            flash("Usuario o clave incorrecto.")
            return redirect("/login")

        # crear la sesion
        session['user'] = user  
        # session['permisos'] = Usuario.get_permisos(user)
        
        config = Configuracion.get_config()
        return render_template("home.html", config=config)

    return render_template("login.html", title='Iniciar Sesión', form=form)


@mod.route("/logout")
def logout():
    if not authenticated(session):
        return redirect("/login")
    # eliminar sesion
    del session['user']
    session.clear()
    flash("La sesión se cerró correctamente.")

    Configuracion.db = get_db()
    config = Configuracion.get_config()
    return render_template("home.html", config=config)