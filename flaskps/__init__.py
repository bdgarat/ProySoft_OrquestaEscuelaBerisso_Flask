from flask import Flask, render_template
from flaskps.config import Config

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template("login.html")
