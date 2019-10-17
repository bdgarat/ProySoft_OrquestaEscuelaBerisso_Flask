from flaskps import app
from flask import redirect, render_template, request, url_for, flash
from flaskps.db import get_db
from flaskps.models.Usuario import Usuario
from flaskps.forms import LoginForm

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
       
    flash("La sesión se inició correctamente.")

    return redirect(url_for('home'))


def logout():
    # eliminar sesion
    # logout_user()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for('home'))
