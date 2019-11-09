from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Estudiante import Estudiante
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import SignUpEstudianteForm, BusquedaEstudianteForm, EditarEstudianteForm
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

@mod.route("/estudiante/registrar", methods=['GET', 'POST'])
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
    if Estudiante.eliminar(id_estudiante):       
        flash('El estudiante se eliminó con éxito')
    
    return redirect('/index/estudiante')

#  EDITAR ESTUDIANTE
@mod.route("/estudiante/editar/<id_estudiante>", methods=['GET', 'POST'])
def editar(id_estudiante):

    # Reviso que tenga permiso
    if 'estudiante_update' not in session['permisos']:
        flash('No tiene permiso para editar estudiantes. ')
        return redirect('/home')  
    else:  
    
        form = EditarEstudianteForm()
        # para manejar los mensajes flash
        error=0
        exito=0
        Estudiante.db = get_db()
        estudiante = Estudiante.get_estudiante(id_estudiante)
        print(estudiante)
        
        if estudiante:

            if request.method == 'POST':
                
                if form.validate_on_submit():
                    Estudiante.editar(id_estudiante, form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.nivel.data, form.domicilio.data, form.genero.data, form.escuela.data, form.tipo_doc.data, form.numero.data, form.tel.data, form.barrio.data)
                    # vuelvo a consultar por los valores del estudiante
                    estudiante = Estudiante.get_estudiante(id_estudiante) 
                    print(estudiante)  
                    flash("Estudiante editado correctamente.")
                    exito = 1
                else:
                    flash("Debe completar todos los campos")
                    error = 1               
           
            # vuelvo a setear el form con los valores actualizados del estudiante
            form.nombre.data = estudiante['nombre']
            form.apellido.data = estudiante['apellido']
            form.fecha_nac.data = estudiante['fecha_nac']
            form.localidad.data = estudiante['localidad_id']
            form.nivel.data = estudiante['nivel_id']
            form.domicilio.data = estudiante['domicilio']
            form.genero.data = estudiante['genero_id']
            form.escuela.data = estudiante['escuela_id']
            form.tipo_doc.data = estudiante['tipo_doc_id']
            form.numero.data = estudiante['numero']
            form.tel.data = estudiante['tel']
            form.barrio.data = estudiante['barrio_id']

            return render_template("estudiantes/editar.html", form=form, error=error, exito=exito)
        else:
            return redirect("/home")

# SHOW ESTUDIANTE
@mod.route("/estudiante/show/<id_estudiante>")
def show(id_estudiante):
    
    # Reviso que tenga permiso
    if 'estudiante_show' in session['permisos']:

        Estudiante.db = get_db()
        estudiante = Estudiante.get_estudiante(id_estudiante)       

        if estudiante:
            
            return render_template("estudiantes/show.html", estudiante=estudiante)
        else:
            return redirect("/home")

    else:
        flash("No tiene permisos para realizar ésta acción")
        return redirect("/home")