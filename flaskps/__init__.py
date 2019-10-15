from flask import Flask, render_template
from flaskps.config import Config
import pymysql

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)


from flaskps import routes