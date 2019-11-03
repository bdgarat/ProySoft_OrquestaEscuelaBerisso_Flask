from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Estudiante import Estudiante
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.helpers.auth import authenticated
from flaskps.forms import SignUpEstudianteForm, BusquedaEstudianteForm
from flask_paginate import Pagination, get_page_parameter



mod = Blueprint('estudiante', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    
    
# LISTADOS
@mod.route("/index/estudiante")
def index_estudiante():

    # Reviso que tenga permiso
    if not Usuario.tengo_permiso(session['permisos'], 'estudiante_index'):
        flash('No tiene permiso para visualizar el listado de estudiantes' )
        return redirect('/home')    

    form = BusquedaEstudianteForm()
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

    Estudiante.db = get_db()
    
    if search:
        # Total registros
        total = Estudiante.get_estudiantes(termino)
        # Consulta usando offset y limit
        estudiantes = Estudiante.get_estudiantes_paginados(per_page, offset, termino)
    else:
        # Total registros
        total = Estudiante.get_estudiantes()
        # Consulta usando offset y limit
        estudiantes = Estudiante.get_estudiantes_paginados(per_page, offset, termino)

    total = len(total)
    if (total == 0 and search == True):
        flash("La búsqueda no obtuvo resultados.")
        error_busqueda = 1
        
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            search=search,
                            found=total,
                            record_name='estudiantes',
                            css_framework='bootstrap4')
    
    return render_template('estudiantes/index.html', 
                            pagination=pagination, 
                            estudiantes=estudiantes,
                            form=form, 
                            error_busqueda=error_busqueda)