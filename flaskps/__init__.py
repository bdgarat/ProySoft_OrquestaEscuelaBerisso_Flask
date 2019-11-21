from flask import Flask, render_template, redirect, session, request
from flaskps.db import get_db
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.config import Config
from flask_session import Session
from flaskps.models.Usuario import Usuario
from flaskps.models.Configuracion import Configuracion

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

#Server Side session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route("/")
@app.route("/home")
def home():
    Configuracion.db = get_db()
    config = Configuracion.get_config()
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")
    return render_template('home.html', config=config)


from flaskps.routes import auth, usuario, configuracion, estudiante, docente, ciclo_lectivo, responsable
app.register_blueprint(auth.mod)
app.register_blueprint(usuario.mod)
app.register_blueprint(configuracion.mod)
app.register_blueprint(estudiante.mod)
app.register_blueprint(docente.mod)
app.register_blueprint(ciclo_lectivo.mod)
app.register_blueprint(responsable.mod)


