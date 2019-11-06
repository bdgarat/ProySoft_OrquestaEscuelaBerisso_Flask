from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Docente import Docente
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import SignUpDocenteForm, BusquedaDocenteForm
from flask_paginate import Pagination, get_page_parameter



mod = Blueprint('docente', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")
    
    
# LISTADOS
@mod.route("/index/docente")
def index_docente():

    # Reviso que tenga permiso
    if 'docente_index' not in session['permisos']:
        flash('No tiene permiso para visualizar el listado de docentes' )
        return redirect('/home')    

    form = BusquedaDocenteForm()
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

    Docente.db = get_db()
    
    if search:
        # Total registros
        total = Docente.get_docentes(termino)
        # Consulta usando offset y limit
        docentes = Docente.get_docentes_paginados(per_page, offset, termino)
    else:
        # Total registros
        total = Docente.get_docentes()
        # Consulta usando offset y limit
        docentes = Docente.get_docentes_paginados(per_page, offset, termino)

    total = len(total)
    if (total == 0 and search == True):
        flash("La búsqueda no obtuvo resultados.")
        error_busqueda = 1
        
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            search=search,
                            found=total,
                            record_name='Docentes',
                            css_framework='bootstrap4')
    
    return render_template('docentes/index.html', 
                            pagination=pagination, 
                            docentes=docentes,
                            form=form, 
                            error_busqueda=error_busqueda)
    
    
# REGISTRAR DOCENTE

@mod.route("/registrar_docente", methods=['GET', 'POST'])
def registrar_docente():
    
   # Reviso que tenga permiso
    if 'docente_new' not in session['permisos']:
        flash('No tiene permiso para registrar docentes. ')
        return redirect('/home')  
    else:  
    
        form = SignUpDocenteForm()
        
        # para manejar los mensajes flash
        error=0
        exito=0
        
        
        if request.method == 'POST':
            
            if form.validate_on_submit():
                Docente.db = get_db()
                    
                docente = Docente(form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.domicilio.data, form.genero.data, form.tipo_doc.data, form.numero.data, form.tel.data)
                Docente.insert(docente)
                
                flash("Docente registrado correctamente.")
                exito = 1
                    
            else: 
                flash("Debe completar todos los campos.")
                error = 1

                
        return render_template("docentes/registrar.html", form=form, error=error, exito=exito)