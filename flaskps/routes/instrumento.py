from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.helpers.auth import authenticated
from flaskps.models.Informacion import Informacion
from flaskps.models.Instrumento import Instrumento
from flaskps.forms import InstrumentoForm
from base64 import b64encode
import base64

mod = Blueprint('instrumento', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")

# REGISTRAR CICLO LECTIVO

@mod.route("/instrumento/registrar", methods=['GET', 'POST'])
def registrar():
    
    # Reviso que tenga permiso
    if 'ciclo_lectivo_new' not in session['permisos']:
        flash('No tiene permiso para crear un ciclos lectivos' )
        return redirect('/home') 
       
    form = InstrumentoForm()
    
    Informacion.db = get_db()
    form.tipo_instrumento.choices = Informacion.all('tipo_instrumento')

    # para manejar los mensajes flash
    error=0
    exito=0

    if request.method == 'POST':
        # IMPORTANTE, CASTEAR A INTEGER 
        form.tipo_instrumento.data = int(form.tipo_instrumento.data)
        
        if form.validate_on_submit():
            
            # Convierto la imagen a base64
            image_string = base64.b64encode(request.files['foto'].read()).decode("utf-8")

            Instrumento.db = get_db()
            # Creo el instrumento
            instrumento = Instrumento(form.nombre.data, form.numero_inventario.data, form.tipo_instrumento.data, image_string)
            Instrumento.insert(instrumento)
            return render_template("instrumentos/prueba.html", foto=image_string)


    return render_template("instrumentos/registrar.html", form=form, error=error, exito=exito)

