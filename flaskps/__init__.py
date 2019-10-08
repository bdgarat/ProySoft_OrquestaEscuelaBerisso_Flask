from flask import Flask, render_template
from flaskps.config import Config

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def hello():
    return render_template('layout.html')