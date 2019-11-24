from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Docente import Docente
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.models.Informacion import Informacion
from flaskps.helpers.auth import authenticated
from flaskps.helpers.apiReferencias import tipos_documento, localidades
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import SignUpDocenteForm, BusquedaDocenteForm, EditarDocenteForm
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

@mod.route("/docente/registrar", methods=['GET', 'POST'])
def registrar_docente():
    
   # Reviso que tenga permiso
    if 'docente_new' not in session['permisos']:
        flash('No tiene permiso para registrar docentes. ')
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
            return render_template("docentes/registrar.html", form=form, error=error, exito=exito, error_api=error_api)
        
        if request.method == 'POST':
            
            # IMPORTANTE, CASTEAR A INTEGER 
            form.genero.data = int(form.genero.data)
            
            if form.validate_on_submit():
                Docente.db = get_db()
                
                # VALIDAR QUE NO EXISTA OTRO TIPO_DOC+NUMERO IGUAL
                existe = Docente.existe_doc(form.tipo_doc.data, form.numero.data)
                if existe:
                    flash("Ya existe un docente con ese documento.")
                    error = 1
                else:                
                    docente = Docente(form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.domicilio.data, form.genero.data, form.tipo_doc.data, form.numero.data, form.tel.data)
                    Docente.insert(docente)
                    
                    flash("Docente registrado correctamente.")
                    exito = 1    
            else: 
                flash("Debe completar todos los campos.")
                error = 1

                
        return render_template("docentes/registrar.html", form=form, error=error, exito=exito, error_api=error_api)
    
    
# ELIMINAR DOCENTE

@mod.route("/docente/eliminar/<id_docente>")
def eliminar(id_docente):

    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para eliminar docentes')
        return redirect('/index/docente')
   
    Docente.db = get_db()
    if Docente.eliminar(id_docente):
        flash('El docente se eliminó con éxito')
    
    return redirect('/index/docente')


#  ACTIVAR/DESACTIVAR DOCENTE
@mod.route("/docente/activar/<id_docente>")
def activar(id_docente):
    # Reviso que tenga permiso
    if 'docente_update' not in session['permisos']:
        flash('No tiene permiso para editar docentes. ')
        return redirect('/index/docente')  

    Docente.db = get_db()
    if Docente.activar(id_docente):
        flash("Se guardaron los cambios con éxito")
    
    return redirect("/index/docente")


#  EDITAR DOCENTE
@mod.route("/docente/editar/<id_docente>", methods=['GET', 'POST'])
def editar(id_docente):

    # Reviso que tenga permiso
    if 'docente_update' not in session['permisos']:
        flash('No tiene permiso para editar docentes. ')
        return redirect('/home')  
    else:  
    

        form = EditarDocenteForm()
        # para manejar los mensajes flash
        error=0
        exito=0
        error_api=0

        Docente.db = get_db()
        docente = Docente.get_docente(id_docente)
        
        # Armo la lista de opciones del select de tipo de documento y localidades
        Informacion.db = get_db()
        form.genero.choices = Informacion.all('genero')

        # Api
        form.tipo_doc.choices = tipos_documento()
        form.localidad.choices = localidades()
        if form.tipo_doc.choices == [] or form.localidad.choices == []:
            flash("No se puede realizar la operación en este momento. Intente más tarde")
            error_api=1
            return render_template("docentes/editar.html", form=form, error=error, exito=exito, error_api=error_api)

        if docente:
            if request.method == 'POST':
            
                # IMPORTANTE, CASTEAR A INTEGER 
                form.genero.data = int(form.genero.data)

                if form.validate_on_submit():
                    
                    # VALIDAR QUE NO EXISTA OTRO TIPO_DOC+NUMERO IGUAL
                    existe = Docente.existe_doc(form.tipo_doc.data, form.numero.data)
                    if existe:
                        flash("Ya existe un docente con ese documento.")
                        error = 1
                    else:
                        Docente.editar(id_docente, form.apellido.data, form.nombre.data, form.fecha_nac.data, form.localidad.data, form.domicilio.data, form.genero.data, form.tipo_doc.data, form.numero.data, form.tel.data)

                        # vuelvo a consultar por los valores del docente
                        docente = Docente.get_docente(id_docente)    
                        flash("Docente editado correctamente.")
                        exito = 1
                else:
                    flash("Debe completar todos los campos")
                    error = 1
            
           
            # vuelvo a setear el form con los valores actualizados del docente
            form.genero.default = docente['genero_id']  
            form.localidad.default = docente['localidad_id']
            form.tipo_doc.default = docente['tipo_doc_id']
            form.process() #IMPORTANTE

            form.nombre.data = docente['nombre']
            form.apellido.data = docente['apellido']
            form.fecha_nac.data = docente['fecha_nac']
            form.domicilio.data = docente['domicilio']
            
            form.numero.data = docente['numero']
            form.tel.data = docente['tel']

            return render_template("docentes/editar.html", form=form, error=error, exito=exito, error_api=error_api)
        else:
            return redirect("/home")


# SHOW DOCENTE
@mod.route("/docente/show/<id_docente>")
def show(id_docente):
    
    # Reviso que tenga permiso
    if 'docente_show' in session['permisos']:

        Docente.db = get_db()
        docente = Docente.get_docente(id_docente)
        tipo_doc=None
        localidad=None
        # API
        error_api = 0
        tipos_doc = tipos_documento()
        loc = localidades()
        if tipos_doc == [] or loc == []:
            flash("No se puede realizar la operación en este momento. Intente más tarde")
            error_api = 1
            return render_template("docentes/show.html", docente=docente, 
                                                        error_api=error_api,
                                                        localidad=localidad,
                                                        tipo_doc=tipo_doc)
        
        tipo_doc = get_nombre_api(tipos_doc, docente['tipo_doc_id'])
        localidad = get_nombre_api(loc, docente['localidad_id'])

        docente = Docente.get_docente_show(id_docente)
        if docente:      
            return render_template("docentes/show.html", docente=docente, 
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