from flask import Flask, render_template
from flaskps.config import Config
from flask_login import LoginManager

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)


# Session manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from flaskps import routes