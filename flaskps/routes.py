from flaskps import app
from flaskps.db import get_db
from flask import render_template
from flaskps.models.usuario import Usuario


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/login")
def login():
    return render_template("login.html")


# prueba
@app.route("/listado")
def listado():
    Usuario.db = get_db()
    usuarios = Usuario.all()

    return render_template('listado.html', usuarios=usuarios)

    