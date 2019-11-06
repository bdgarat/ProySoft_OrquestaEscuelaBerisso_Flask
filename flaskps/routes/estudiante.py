from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Estudiante import Estudiante
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import SignUpEstudianteForm, BusquedaEstudianteForm
from flask_paginate import Pagination, get_page_parameter



mod = Blueprint('estudiante', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")
    
    
# LISTADOS
@mod.route("/index/estudiante")
def index_estudiante():

    # Reviso que tenga permiso
    if 'estudiante_index' not in session['permisos']:
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
    
    
# REGISTRAR ESTUDIANTE

@mod.route("/registrar_estudiante", methods=['GET', 'POST'])
def registrar_estudiante():
    
   # Reviso que tenga permiso
    if 'estudiante_new' not in session['permisos']:
        flash('No tiene permiso para registrar estudiantes. ')
        return redirect('/home')  
    else:  
    
        form = SignUpEstudianteForm()
        
        # para manejar los mensajes flash
        error=0
        exito=0
        
        
        if request.method == 'POST':
            
            if form.validate_on_submit():
                Estudiante.db = get_db()
                    
                estudiante = Estudiante(form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.nivel.data, form.domicilio.data, form.genero.data, form.escuela.data, form.tipo_doc.data, form.numero.data, form.tel.data, form.barrio.data)
                Estudiante.insert(estudiante)
                
                flash("Estudiante registrado correctamente.")
                exito = 1
                    
            else: 
                flash("Debe completar todos los campos.")
                error = 1

                
        return render_template("estudiantes/registrar.html", form=form, error=error, exito=exito)
    
    
# ELIMINAR ESTUDIANTE

@mod.route("/estudiante/eliminar/<id_estudiante>")
def eliminar(id_estudiante):

    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para eliminar estudiantes')
        return redirect('/index/estudiante')
   
    Estudiante.db = get_db()
    Estudiante.eliminar(id_estudiante)
    flash('El estudiante se eliminó con éxito')
    
    return redirect('/index/estudiante')