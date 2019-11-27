from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.helpers.auth import authenticated
from flaskps.models.Informacion import Informacion
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Instrumento import Instrumento
from flaskps.forms import InstrumentoForm, BusquedaInstrumentoForm
from flask_paginate import Pagination, get_page_parameter
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


# LISTADOS
@mod.route("/index/instrumento")
def index_instrumento():

    # Reviso que tenga permiso
    if 'instrumento_index' not in session['permisos']:
        flash('No tiene permiso para visualizar el listado de instrumentos' )
        return redirect('/home')    

    form = BusquedaInstrumentoForm()
    error_busqueda = 0

    search = False
    termino = request.args.get('termino')
    
    if termino:
        search = True

    # seteo el value del input si vino con algo
    form.termino.data = termino
    
    # Setear variables de paginacion
    Configuracion.db = get_db()
    per_page = Configuracion.get_paginacion()['paginacion']
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    Instrumento.db = get_db()
    
    if search:
        # Total registros
        total = Instrumento.get_instrumentos(termino)
        # Consulta usando offset y limit
        instrumentos = Instrumento.get_instrumentos_paginados(per_page, offset, termino)
    else:
        # Total registros
        total = Instrumento.get_instrumentos()
        # Consulta usando offset y limit
        instrumentos = Instrumento.get_instrumentos_paginados(per_page, offset)

    total = len(total)
    for i in instrumentos:
        i['foto'] = i['foto'].decode('utf8')

            
    if (total == 0 and search == True):
        flash("La búsqueda no obtuvo resultados.")
        error_busqueda = 1
        
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            search=search,
                            found=total,
                            record_name='instrumentos',
                            css_framework='bootstrap4')
    
    return render_template('instrumentos/index.html', 
                            pagination=pagination, 
                            instrumentos=instrumentos,
                            form=form, 
                            error_busqueda=error_busqueda)






# REGISTRAR INSTRUMENTO
@mod.route("/instrumento/registrar", methods=['GET', 'POST'])
def registrar():
    
    # Reviso que tenga permiso
    if 'instrumento_new' not in session['permisos']:
        flash('No tiene permiso para crear instrumentos' )
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

