from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Estudiante import Estudiante
from flaskps.models.Informacion import Informacion
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.helpers.auth import authenticated
from flaskps.helpers.apiReferencias import tipos_documento, localidades
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
        Estudiante.db = get_db()
        
        # para manejar los mensajes flash
        error=0
        exito=0
        error_api=0
        
        # Armo la lista de opciones del select de tipo de documento y localidades
        Informacion.db = get_db()
        form.barrio.choices = Informacion.all('barrio')
        form.genero.choices = Informacion.all('genero')
        form.nivel.choices = Informacion.all('nivel')
        form.escuela.choices = Informacion.all('escuela')
        form.tipo_responsable.choices = Informacion.all('tipo_responsable')
        form.responsable.choices = Estudiante.get_responsables_select()
        

        # Api
        form.tipo_doc.choices = tipos_documento()
        form.localidad.choices = localidades()
        if form.tipo_doc.choices == [] or form.localidad.choices == []:
            flash("No se puede realizar la operación en este momento. Intente más tarde")
            error_api=1
            return render_template("estudiantes/registrar.html", form=form, error=error, exito=exito, error_api=error_api)


        
        

        if request.method == 'POST':
            
            # IMPORTANTE, CASTEAR A INTEGER 
            form.genero.data = int(form.genero.data)
            form.nivel.data = int(form.nivel.data)
            form.tipo_responsable.data = int(form.tipo_responsable.data)
            form.responsable.data = int(form.responsable.data)
            form.escuela.data = int(form.escuela.data)
            form.barrio.data = int(form.barrio.data)
            
            if form.validate_on_submit():
                    
                estudiante = Estudiante(form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.nivel.data, form.domicilio.data, form.genero.data, form.escuela.data, form.tipo_doc.data, form.numero.data, form.tel.data, form.barrio.data)
                id_estudiante = Estudiante.insert(estudiante)

                Estudiante.agregar_responsable(form.responsable.data, id_estudiante, form.tipo_responsable.data)

                flash("Estudiante registrado correctamente.")
                exito = 1
                    
            else: 
                flash("Debe completar todos los campos.")
                error = 1

                
        return render_template("estudiantes/registrar.html", form=form, error=error, exito=exito, error_api=error_api)
    
    
# ELIMINAR ESTUDIANTE

@mod.route("/estudiante/eliminar/<id_estudiante>")
def eliminar(id_estudiante):

    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para desactivar estudiantes')
        return redirect('/index/estudiante')
   
    Estudiante.db = get_db()
    if Estudiante.eliminar(id_estudiante):       
        flash('El estudiante se desactivó con éxito')
    
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
        error_api=0

        Estudiante.db = get_db()
        estudiante = Estudiante.get_estudiante(id_estudiante)
        responsable = Estudiante.get_responsable(id_estudiante)

        # Armo la lista de opciones del select de tipo de documento y localidades
        Informacion.db = get_db()
        form.barrio.choices = Informacion.all('barrio')
        form.genero.choices = Informacion.all('genero')
        form.nivel.choices = Informacion.all('nivel')
        form.escuela.choices = Informacion.all('escuela')
        form.tipo_responsable.choices = Informacion.all('tipo_responsable')
        form.responsable.choices = Estudiante.get_responsables_select()
        

        # Api
        form.tipo_doc.choices = tipos_documento()
        form.localidad.choices = localidades()
        if form.tipo_doc.choices == [] or form.localidad.choices == []:
            flash("No se puede realizar la operación en este momento. Intente más tarde")
            error_api=1
            return render_template("estudiantes/editar.html", form=form, error=error, exito=exito, error_api=error_api)
        
        if estudiante:

            if request.method == 'POST':
                
                # IMPORTANTE, CASTEAR A INTEGER 
                form.genero.data = int(form.genero.data)
                form.nivel.data = int(form.nivel.data)
                form.tipo_responsable.data = int(form.tipo_responsable.data)
                form.responsable.data = int(form.responsable.data)
                form.escuela.data = int(form.escuela.data)
                form.barrio.data = int(form.barrio.data)


                if form.validate_on_submit():
                    Estudiante.editar(id_estudiante, form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.nivel.data, form.domicilio.data, form.genero.data, form.escuela.data, form.tipo_doc.data, form.numero.data, form.tel.data, form.barrio.data)
                    
                    if form.responsable.data != responsable['id'] or form.tipo_responsable.data != responsable['tipo_responsable_id']:
                        Estudiante.editar_responsable(form.responsable.data, id_estudiante, form.tipo_responsable.data)

                    # vuelvo a consultar por los valores del estudiante
                    estudiante = Estudiante.get_estudiante(id_estudiante) 
                    responsable = Estudiante.get_responsable(id_estudiante)

                    flash("Estudiante editado correctamente.")
                    exito = 1
                else:
                    flash("Debe completar todos los campos")
                    error = 1               
           
            # vuelvo a setear el form con los valores actualizados del estudiante
            form.genero.default = estudiante['genero_id']  
            form.localidad.default = estudiante['localidad_id']
            form.tipo_doc.default = estudiante['tipo_doc_id']
            form.escuela.default = estudiante['escuela_id']
            form.nivel.default = estudiante['nivel_id']
            form.barrio.default = estudiante['barrio_id']
            form.tipo_responsable.default = responsable['tipo_responsable_id']
            form.responsable.default = responsable['id']
            form.process() #IMPORTANTE

            form.nombre.data = estudiante['nombre']
            form.apellido.data = estudiante['apellido']
            form.fecha_nac.data = estudiante['fecha_nac']
            form.domicilio.data = estudiante['domicilio']
            form.numero.data = estudiante['numero']
            form.tel.data = estudiante['tel']

            return render_template("estudiantes/editar.html", form=form, error=error, exito=exito, error_api=error_api)
        else:
            return redirect("/home")

# SHOW ESTUDIANTE
@mod.route("/estudiante/show/<id_estudiante>")
def show(id_estudiante):
    
    # Reviso que tenga permiso
    if 'estudiante_show' in session['permisos']:

        Estudiante.db = get_db()
        estudiante = Estudiante.get_estudiante(id_estudiante)
        responsable = Estudiante.get_responsable(id_estudiante)
        tipo_doc=None
        localidad=None
        # API
        error_api = 0
        tipos_doc = tipos_documento()
        loc = localidades()

        if tipos_doc == [] or loc == []:
            flash("No se puede realizar la operación en este momento. Intente más tarde")
            error_api = 1
            return render_template("estudiantes/show.html", estudiante=estudiante, 
                                                            responsable=responsable, 
                                                            error_api=error_api,
                                                            localidad=localidad,
                                                            tipo_doc=tipo_doc)
        
        tipo_doc = get_nombre_api(tipos_doc, estudiante['tipo_doc_id'])
        localidad = get_nombre_api(loc, estudiante['localidad_id'])      
        
        estudiante = Estudiante.get_estudiante_show(id_estudiante)               

        if estudiante:
            
            return render_template("estudiantes/show.html", estudiante=estudiante, 
                                                            responsable=responsable, 
                                                            error_api=error_api,
                                                            localidad=localidad,
                                                            tipo_doc=tipo_doc)
        else:
            return redirect("/home")

    else:
        flash("No tiene permisos para realizar ésta acción")
        return redirect("/home")


# OPERACIONES
def get_nombre_api(lista, id):
    for t in lista:
        if int(t[0]) == int(id):
            return t[1]
    return None