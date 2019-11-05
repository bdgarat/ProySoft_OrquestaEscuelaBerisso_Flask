from flask import Flask, render_template, redirect
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

#Esto lo dejo pero en realidad no funciona porque no es dinamico, para ver los cambios hay que 
# bajar y subir el server 

# with app.app_context():
#     # Si el modo deshabilitado del sitio está activado, se muestra el template de "Sitio en Mantenimiento"
#     Configuracion.db = get_db()
#     habilitado = Configuracion.get_sitio_habilitado()['sitio_habilitado']

habilitado = None
@app.before_request
def before_request():
    Configuracion.db = get_db()
    habilitado = Configuracion.get_sitio_habilitado()['sitio_habilitado']
    if habilitado == 0:
        return render_template('mantenimiento.html')

@app.route("/")
@app.route("/home")
def home():
    Configuracion.db = get_db()
    config = Configuracion.get_config()
    return render_template('home.html', config=config)


from flaskps.routes import auth, usuario, configuracion, estudiante, docente
app.register_blueprint(auth.mod)
app.register_blueprint(usuario.mod)
app.register_blueprint(configuracion.mod)
app.register_blueprint(estudiante.mod)
app.register_blueprint(docente.mod)

