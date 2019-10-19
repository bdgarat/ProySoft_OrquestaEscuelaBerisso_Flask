from flaskps import app
from flask import redirect, render_template, request, url_for, flash, abort, session
from flaskps.db import get_db
from flaskps.models.Usuario import Usuario
from flaskps.forms import LoginForm
from flaskps.helpers.auth import authenticated

def login():
    form = LoginForm()
    return render_template("login.html", title='Iniciar Sesión', form=form)

def authenticate():
    params = request.form

    Usuario.db = get_db()
    user = Usuario.find_by_email_and_pass(params['email'], params['password'])

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for('iniciar_sesion'))

    # crear la sesion
    session['user'] = user['email']   
    flash("La sesión se inició correctamente.")

    return redirect(url_for('home'))


def logout():
    # eliminar sesion
    # logout_user()
    del session['user']
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for('home'))

def isLogged():
    if authenticated(session):
        flash("Usted esta logueado actualmente")
    else:
        flash("Usted NO esta logueado")
    return redirect(url_for('home'))