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
            Instrumento.db = get_db()
            # VALIDAR QUE NO EXISTA OTRO NUMERO INVENTARIO
            existe = Instrumento.existe(form.numero_inventario.data)
            if existe:
                flash("Ya existe un instrumento con ese numero de inventario.")
                error = 1
                return render_template("instrumentos/registrar.html", form=form, error=error, exito=exito)
            else:
                # Convierto la imagen a base64
                image_string = base64.b64encode(request.files['foto'].read()).decode("utf-8")
                # Creo el instrumento
                instrumento = Instrumento(form.nombre.data, form.numero_inventario.data, form.tipo_instrumento.data, image_string)
                Instrumento.insert(instrumento)
                flash("Instrumento registrado correctamente.")
                exito = 1
        else: 
            flash("Debe completar todos los campos.")
            error = 1

    return render_template("instrumentos/registrar.html", form=form, error=error, exito=exito)


# ELIMINAR INSTRUMENTO
@mod.route("/instrumento/eliminar/<id_instrumento>")
def eliminar(id_instrumento):

    # Reviso que tenga permiso
    if 'instrumento_destroy' not in session['permisos']:
        flash('No tiene permiso para eliminar instrumentos' )
        return redirect('/index/instrumento') 
   
    Instrumento.db = get_db()
    if Instrumento.eliminar(id_instrumento):       
        flash('El instrumento se eliminó con éxito')
    
    return redirect('/index/instrumento')

# EDITAR INSTRUMENTO
@mod.route("/instrumento/editar/<id_instrumento>", methods=['GET', 'POST'])
def editar(id_instrumento):
    
    # Reviso que tenga permiso
    if 'instrumento_update' not in session['permisos']:
        flash('No tiene permiso para editar instrumentos' )
        return redirect('/index/instrumento') 

    form = InstrumentoForm()
    
    Informacion.db = get_db()
    form.tipo_instrumento.choices = Informacion.all('tipo_instrumento')

    # para manejar los mensajes flash
    error=0
    exito=0
    
    Instrumento.db = get_db()
    instrumento = Instrumento.get_instrumento(id_instrumento)

    if instrumento:

        if request.method == 'POST':
            
            # VALIDAR QUE NO EXISTA OTRO NUMERO INVENTARIO
            existe = Instrumento.existe(form.numero_inventario.data)
            if existe and int(existe['id']) != int(id_instrumento):
                flash("Ya existe un instrumento con ese numero de inventario.")
                error = 1
            else:
                # Convierto la imagen a base64
                image_string = base64.b64encode(request.files['foto'].read()).decode("utf-8")
                Instrumento.editar(id_instrumento, form.nombre.data, form.numero_inventario.data, form.tipo_instrumento.data, image_string)
                # vuelvo a consultar por los valores del instrumento
                instrumento = Instrumento.get_instrumento(id_instrumento)
                flash("Instrumento modificado correctamente.")
                exito = 1
                    
                
        # vuelvo a setear el form con los valores actualizados del instrumento
        form.tipo_instrumento.default = instrumento['tipo_id']
        form.process() #IMPORTANTE
        form.nombre.data = instrumento['nombre']
        form.numero_inventario.data = instrumento['numero_inventario']

        return render_template("instrumentos/editar.html", form=form, error=error, exito=exito)
    else:
        return redirect("/home")



# SHOW INSTRUMENTO
@mod.route("/instrumento/show/<id_instrumento>")
def show(id_instrumento):
    # Reviso que tenga permiso
    if 'instrumento_show' not in session['permisos']:
        flash('No tiene permiso para visualizar instrumentos' )
        return redirect('/index/instrumento')
    
    Instrumento.db = get_db()
    instrumento = Instrumento.get_instrumento(id_instrumento)    
    instrumento['foto'] = instrumento['foto'].decode('utf8')

    return render_template("instrumentos/show.html", instrumento=instrumento)
    