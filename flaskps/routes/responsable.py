from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Responsable import Responsable
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.models.Informacion import Informacion
from flaskps.helpers.auth import authenticated
from flaskps.helpers.apiReferencias import tipos_documento, localidades
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import SignUpDocenteForm, BusquedaDocenteForm, EditarDocenteForm
from flask_paginate import Pagination, get_page_parameter



mod = Blueprint('responsable', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")
    
    
# LISTADOS
@mod.route("/index/responsable")
def index_responsable():

    # Reviso que tenga permiso
    if 'estudiante_index' not in session['permisos']:
        flash('No tiene permiso para visualizar el listado de responsables' )
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

    Responsable.db = get_db()
    
    if search:
        # Total registros
        total = Responsable.get_responsables(termino)
        # Consulta usando offset y limit
        responsables = Responsable.get_responsables_paginados(per_page, offset, termino)
    else:
        # Total registros
        total = Responsable.get_responsables()
        # Consulta usando offset y limit
        responsables = Responsable.get_responsables_paginados(per_page, offset, termino)

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
    
    return render_template('responsables/index.html', 
                            pagination=pagination, 
                            responsables=responsables,
                            form=form, 
                            error_busqueda=error_busqueda)
    
    
# REGISTRAR RESPONSABLE

@mod.route("/responsable/registrar", methods=['GET', 'POST'])
def registrar_responsable():
    
   # Reviso que tenga permiso
    if 'estudiante_new' not in session['permisos']:
        flash('No tiene permiso para registrar responsables. ')
        return redirect('/home')  
    else:  
    
        form = SignUpDocenteForm(request.form)
        
        # para manejar los mensajes flash
        error=0
        exito=0
        error_api=0
        
        # Armo la lista de opciones del select de tipo de documento y localidades
        Informacion.db = get_db()
        form.genero.choices = Informacion.all('genero')

        # Api
        form.tipo_doc.choices = tipos_documento()
        form.localidad.choices = localidades()
        if form.tipo_doc.choices == [] or form.localidad.choices == []:
            flash("No se puede realizar la operación en este momento. Intente más tarde")
            error_api=1
            return render_template("responsables/registrar.html", form=form, error=error, exito=exito, error_api=error_api)

        if request.method == 'POST':
            
            # IMPORTANTE, CASTEAR A INTEGER 
            form.genero.data = int(form.genero.data)
            
            if form.validate_on_submit():
                Responsable.db = get_db()
                # VALIDAR QUE NO EXISTA OTRO TIPO_DOC+NUMERO IGUAL
                existe = Responsable.existe_doc(form.tipo_doc.data, form.numero.data)
                if existe:
                    flash("Ya existe un responsable con ese documento.")
                    error = 1
                else:
                    responsable = Responsable(form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.domicilio.data, form.genero.data, form.tipo_doc.data, form.numero.data, form.tel.data)
                    Responsable.insert(responsable)
                    flash("Responsable registrado correctamente.")
                    exito = 1
                    
            else: 
                flash("Debe completar todos los campos.")
                error = 1

                
        return render_template("responsables/registrar.html", form=form, error=error, exito=exito, error_api=error_api)
    
    
# ELIMINAR RESPONSABLE
@mod.route("/responsable/eliminar/<id_responsable>")
def eliminar(id_responsable):

    # Reviso que tenga permiso
    if 'estudiante_destroy' not in session['roles']:
        flash('No tiene permiso para eliminar responsables')
        return redirect('/index/responsable')
   
    Responsable.db = get_db()
    if Responsable.eliminar(id_responsable):
        flash('El responsable se eliminó con éxito')
    
    return redirect('/index/responsable')

#  EDITAR RESPONSABLE
@mod.route("/responsable/editar/<id_responsable>", methods=['GET', 'POST'])
def editar(id_responsable):

    # Reviso que tenga permiso
    if 'estudiante_update' not in session['permisos']:
        flash('No tiene permiso para editar responsable. ')
        return redirect('/home')  
    else:  
    

        form = EditarDocenteForm()
        # para manejar los mensajes flash
        error=0
        exito=0
        error_api=0
        Responsable.db = get_db()
        responsable = Responsable.get_responsable(id_responsable)
        
        # Armo la lista de opciones del select de tipo de documento y localidades
        Informacion.db = get_db()
        form.genero.choices = Informacion.all('genero')

        # Api
        form.tipo_doc.choices = tipos_documento()
        form.localidad.choices = localidades()
        if form.tipo_doc.choices == [] or form.localidad.choices == []:
            flash("No se puede realizar la operación en este momento. Intente más tarde")
            error_api=1
            return render_template("responsables/editar.html", form=form, error=error, exito=exito, error_api=error_api)

        if responsable:
            if request.method == 'POST':
            
                # IMPORTANTE, CASTEAR A INTEGER 
                form.genero.data = int(form.genero.data)

                if form.validate_on_submit():

                    # VALIDAR QUE NO EXISTA OTRO TIPO_DOC+NUMERO IGUAL
                    existe = Responsable.existe_doc(form.tipo_doc.data, form.numero.data)
                    if existe and int(existe['id']) != int(id_responsable):
                        flash("Ya existe un responsable con ese documento.")
                        error = 1
                    else:    
                        Responsable.editar(id_responsable, form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.domicilio.data, form.genero.data, form.tipo_doc.data, form.numero.data, form.tel.data)

                        # vuelvo a consultar por los valores del docente
                        responsable = Responsable.get_responsable(id_responsable)    
                        flash("Responsable editado correctamente.")
                        exito = 1
                else:
                    flash("Debe completar todos los campos")
                    error = 1
            
           
            # vuelvo a setear el form con los valores actualizados del docente
            form.genero.default = responsable['genero_id']  
            form.localidad.default = responsable['localidad_id']
            form.tipo_doc.default = responsable['tipo_doc_id']
            form.process() #IMPORTANTE

            form.nombre.data = responsable['nombre']
            form.apellido.data = responsable['apellido']
            form.fecha_nac.data = responsable['fecha_nac']
            form.domicilio.data = responsable['domicilio']
            
            form.numero.data = responsable['numero']
            form.tel.data = responsable['tel']

            return render_template("responsables/editar.html", form=form, error=error, exito=exito, error_api=error_api)
        else:
            return redirect("/home")


# SHOW RESPONSABLE
@mod.route("/responsable/show/<id_responsable>")
def show(id_responsable):
    
    # Reviso que tenga permiso
    if 'estudiante_show' in session['permisos']:

        Responsable.db = get_db()
        responsable = Responsable.get_responsable(id_responsable)
        tipo_doc=None
        localidad=None

        # API
        error_api = 0
        tipos_doc = tipos_documento()
        loc = localidades()
        if tipos_doc == [] or loc == []:
            flash("No se puede realizar la operación en este momento. Intente más tarde")
            error_api = 1
            return render_template("responsables/show.html", responsable=responsable, 
                                                                error_api=error_api,
                                                                localidad=localidad,
                                                                tipo_doc=tipo_doc)

        tipo_doc = get_nombre_api(tipos_doc, responsable['tipo_doc_id'])
        localidad = get_nombre_api(loc, responsable['localidad_id'])

        responsable = Responsable.get_responsable_show(id_responsable)
        if responsable:      
            return render_template("responsables/show.html", responsable=responsable, 
                                                        error_api=error_api,
                                                        localidad=localidad,
                                                        tipo_doc=tipo_doc )
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