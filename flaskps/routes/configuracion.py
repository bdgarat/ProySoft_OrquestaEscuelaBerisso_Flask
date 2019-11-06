from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible 
from flaskps.forms import ConfigForm

mod = Blueprint('configuracion', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso que tenga permiso para ver config
    if ( 'config_index' ) not in session['permisos']:
        flash('No tiene permiso para ver la configuración del sistema')
        return redirect('/home')
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")


# RUTAS
@mod.route("/mantenimiento")
def mantenimiento():
    return render_template("mantenimiento.html")

@mod.route("/config", methods=['GET', 'POST'])
def config():
    form = ConfigForm()
    Configuracion.db = get_db()   
    config_actual = Configuracion.get_config()
    
    # para manejar los mensajes flash
    error=0
    exito=0
    if request.method == 'POST':
        
        # Problema: el formulario solo pasa la validacion si escribo algo en el campo 'paginacion', si lo dejo vacio no pasa

        if form.validate_on_submit():
            Configuracion.set_config( Configuracion( form.titulo.data, form.descripcion.data, form.contacto.data, form.paginacion.data, form.sitio_habilitado.data) )
            config_actual = Configuracion.get_config()     
            flash("Se actualizó la información con éxito")
            exito=1
        else:
            flash("Debe completar el campo 'paginación' con un valor numérico")
            error=1


    # seteo el value de los inputs con la configuracion ya cargada en la bd
    form.titulo.data = config_actual['titulo']
    form.descripcion.data = config_actual['descripcion']
    form.contacto.data = config_actual['contacto']
    form.paginacion.data = config_actual['paginacion']
    form.sitio_habilitado.data = config_actual['sitio_habilitado']

    
    return render_template("usuarios/config.html", form=form, config=config_actual, error=error, exito=exito)

