from flask import Flask, render_template
from flaskps.config import Config
from flask_session import Session

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

#Server Side session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


from flaskps.routes import auth, usuario
app.register_blueprint(auth.mod)
app.register_blueprint(usuario.mod)

