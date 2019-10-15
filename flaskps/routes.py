from flaskps import app
from flaskps.db import get_db
from flask import render_template, flash, redirect
from flaskps.models.Usuario import Usuario
from flaskps.forms import LoginForm


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        return redirect("/home")
    return render_template("login.html", title='Iniciar Sesión', form=form)


# prueba
@app.route("/listado")
def listado():
    Usuario.db = get_db()
    usuarios = Usuario.all()

    return render_template('listado.html', usuarios=usuarios)

# prueba
@app.route("/insertar")
def insertar():
    Usuario.db = get_db()
    u = Usuario('mel@gmail.com', 'melisa', '0123', 'melisa', 'onofri')
    ok = Usuario.insert(u)
    if (ok):
        return render_template('insertar.html', usuario = u)


    