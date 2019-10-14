from flask import Flask, render_template
from flaskps.config import Config
import pymysql

# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

# Conexion con la base de datos
# ejecutar db.cursor() para usarla
db = pymysql.connect(host=Config.DB_HOST, 
                             user=Config.DB_USER, 
                             password=Config.DB_PASS, 
                             db=Config.DB_NAME)


from flaskps import routes