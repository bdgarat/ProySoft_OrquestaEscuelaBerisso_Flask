from flask import Flask, render_template
from flaskps.db import get_db
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
    return render_template('home.html', config=config)


from flaskps.routes import auth, usuario
app.register_blueprint(auth.mod)
app.register_blueprint(usuario.mod)

