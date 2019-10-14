from flask import Flask, render_template
from flaskps.config import Config
import pymysql

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

# Conexion con la base de datos
# ejecutar connection.cursor() para usarla
connection = pymysql.connect(host=Config.DB_HOST, 
                             user=Config.DB_USER, 
                             password=Config.DB_PASS, 
                             db=Config.DB_NAME)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template("login.html")
