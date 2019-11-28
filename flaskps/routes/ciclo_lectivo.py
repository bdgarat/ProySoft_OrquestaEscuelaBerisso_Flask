from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Ciclo_lectivo import Ciclo_lectivo
from flaskps.models.Docente import Docente
from flaskps.models.Taller import Taller
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.models.Informacion import Informacion
from flaskps.helpers.auth import authenticated
from flaskps.helpers.apiReferencias import tipos_documento, localidades
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import SignUpCicloLectivoForm, BusquedaCicloLectivoForm, EditarCicloLectivoForm, BusquedaTallerForm
from flask_paginate import Pagination, get_page_parameter



mod = Blueprint('ciclo_lectivo', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")
    
    
# LISTADOS
@mod.route("/index/ciclo_lectivo")
def index_ciclo_lectivo():

    # Reviso que tenga permiso
    if 'ciclo_lectivo_index' not in session['permisos']:
        flash('No tiene permiso para visualizar el listado de ciclos lectivos' )
        return redirect('/home')    

    form = BusquedaCicloLectivoForm()
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

    Ciclo_lectivo.db = get_db()
    
    if search:
        # Total registros
        total = Ciclo_lectivo.get_ciclos_lectivos(termino)
        # Consulta usando offset y limit
        ciclos_lectivos = Ciclo_lectivo.get_ciclos_lectivos_paginados(per_page, offset, termino)
    else:
        # Total registros
        total = Ciclo_lectivo.get_ciclos_lectivos()
        # Consulta usando offset y limit
        ciclos_lectivos = Ciclo_lectivo.get_ciclos_lectivos_paginados(per_page, offset, termino)

    total = len(total)
    if (total == 0 and search == True):
        flash("La búsqueda no obtuvo resultados.")
        error_busqueda = 1
        
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            search=search,
                            found=total,
                            record_name='ciclos_lectivos',
                            css_framework='bootstrap4')
    
    return render_template('ciclos_lectivos/index.html', 
                            pagination=pagination, 
                            ciclos_lectivos=ciclos_lectivos,
                            form=form, 
                            error_busqueda=error_busqueda)
    
# REGISTRAR CICLO LECTIVO

@mod.route("/ciclo_lectivo/registrar", methods=['GET', 'POST'])
def registrar():
    
    # Reviso que tenga permiso
    if 'ciclo_lectivo_new' not in session['permisos']:
        flash('No tiene permiso para crear un ciclos lectivos' )
        return redirect('/home') 
       
    form = SignUpCicloLectivoForm()
    semestres = []
    semestres.append(('1', 'Semestre 1'))
    semestres.append(('2', 'Semestre 2'))
    form.semestre.choices = semestres

    # para manejar los mensajes flash
    error=0
    exito=0
    
    if request.method == 'POST':
        
        if form.validate_on_submit():
            
            Ciclo_lectivo.db = get_db()
            
            # chequeo que no exista ya un ciclo lectivo creado para ese semestere y año
            existe = Ciclo_lectivo.existe(form.semestre.data, form.fecha_ini.data.year)
            if existe:
                flash("Ya existe un ciclo lectivo creado para esas fechas y semestre.")
                error = 1
                return render_template("ciclos_lectivos/registrar.html", form=form, error=error, exito=exito)
            
            # SI NO EXISTE Y QUEIRO CREAR UN SEMESTRE 2, CHEQUEO SI HAY SEMESTRE 1, Y SI HAY, CHEQUEO QUE NO HAYA PROBLEMA CON LAS FECHAS
            
            if (form.semestre.data == '2'):
                if Ciclo_lectivo.existe('1', form.fecha_ini.data.year):
                    print("existe sem 1")
                    # chequeo que no se superpongan las fechas
                    if Ciclo_lectivo.se_superponen(form.fecha_ini.data):
                        flash("La fecha de inicio del semestre 2 se superpone con la fecha de fin del semestre 1 registrado para ese año.")
                        error = 1
                        return render_template("ciclos_lectivos/registrar.html", form=form, error=error, exito=exito)
            
            
            if (form.fecha_fin.data < form.fecha_ini.data):
                error=1
                flash("La fecha de fin del ciclo lectivo debe ser mayor a la fecha de inicio del mismo") 
                return render_template("ciclos_lectivos/registrar.html", form=form, error=error, exito=exito)
            
            # ESTÁ BIEN, LO CREO
            ciclo_lectivo = Ciclo_lectivo(form.fecha_ini.data, form.fecha_fin.data, form.semestre.data)
                
            Ciclo_lectivo.insert(ciclo_lectivo)
            
            flash("Ciclo lectivo registrado correctamente.")
            exito = 1
                            
        else: 
            flash("Debe completar todos los campos")
            error = 1
            
    return render_template("ciclos_lectivos/registrar.html", form=form, error=error, exito=exito)
    
# ELIMINAR CICLO LECTIVO

@mod.route("/ciclo_lectivo/eliminar/<id_ciclo_lectivo>")
def eliminar(id_ciclo_lectivo):

    # Reviso que tenga permiso
    if 'ciclo_lectivo_index' not in session['permisos']:
        flash('No tiene permiso para eliminar un ciclo lectivo.' )
        return redirect('/home')
   
    Ciclo_lectivo.db = get_db()
    if Ciclo_lectivo.eliminar(id_ciclo_lectivo):
        flash('El ciclo lectivo se eliminó con éxito.')
    
    return redirect('/index/ciclo_lectivo')


# VER CICLO LECTIVO CON SUS TALLERES
@mod.route("/ciclo_lectivo/show/<id_ciclo>")
def show(id_ciclo):
    
    # Reviso que tenga permiso
    if 'ciclo_lectivo_show' not in session['permisos']:
        flash('No tiene permiso para ver la información de los ciclos lectivos.' )
        return redirect('/home') 
    
    Ciclo_lectivo.db = get_db()
    
    ciclo = Ciclo_lectivo.get_ciclo_lectivo(id_ciclo)
    
    if ciclo:
        # BUSCO LOS TALLERES PAGINADOS
        
        form = BusquedaTallerForm()
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
        
        Taller.db = get_db()
        if search:
            # Total registros
            total = Taller.get_talleres_por_ciclo(id_ciclo, termino)
            # Consulta usando offset y limit
            talleres = Taller.get_talleres_por_ciclo_paginados(per_page, id_ciclo, offset, termino)
        else:
            # Total registros
            total = Taller.get_talleres_por_ciclo(id_ciclo)
            # Consulta usando offset y limit
            talleres = Taller.get_talleres_por_ciclo_paginados(per_page,id_ciclo,offset)

        total = len(total)
        if (total == 0 and search == True):
            flash("La búsqueda no obtuvo resultados.")
            error_busqueda = 1
            
        pagination = Pagination(page=page, 
                                per_page=per_page, 
                                total=total,
                                search=search,
                                found=total,
                                record_name='ciclos_lectivos',
                                css_framework='bootstrap4')
        return render_template("ciclos_lectivos/show.html", form = form, ciclo = ciclo, pagination = pagination, talleres = talleres, error_busqueda = error_busqueda)
    
    return redirect('/home')


@mod.route("/ciclo_lectivo/insertar_docente_en_taller", methods=['GET'])
def insertar_docente_en_taller():
    # Reviso que tenga permiso
    if 'ciclo_lectivo_update' not in session['permisos']:
        flash('No tiene permiso para agregar un docente al ciclo lectivo' )
        return redirect('/home') 

    Taller.db = get_db()
    id_ciclo = request.args.get('ciclo', None)
    id_taller = request.args.get('taller', None)
    id_docente = request.args.get('docente', None)
    if not Taller.existe_docente_en_taller(id_ciclo, id_taller, id_docente):
        if Taller.insertar_docente_en_taller(id_ciclo, id_taller, id_docente):
            flash("El docente ha sido insertado correctamente")
    else:
        flash("El docente ya ha sido insertado en el taller!")
    return redirect('/index/ciclo_lectivo')


@mod.route("/ciclo_lectivo/insertar_estudiante_en_taller", methods=['GET'])
def insertar_estudiante_en_taller():
    # Reviso que tenga permiso
    if 'ciclo_lectivo_update' not in session['permisos']:
        flash('No tiene permiso para agregar un docente al ciclo lectivo' )
        return redirect('/home') 

    Taller.db = get_db()
    id_ciclo = request.args.get('ciclo', None)
    id_taller = request.args.get('taller', None)
    id_estudiante = request.args.get('estudiante', None)
    if not Taller.existe_estudiante_en_taller(id_ciclo, id_taller, id_estudiante):
        if Taller.insertar_estudiante_en_taller(id_ciclo, id_taller, id_estudiante):
            flash("El estudiante ha sido insertado correctamente")
    else:
        flash('El estudiante ya ha sido insertado en el taller!' ) 

    return redirect('/index/ciclo_lectivo')


@mod.route("/ciclo_lectivo/insertar_taller", methods=['GET'])
def insertar_taller_en_ciclo():
    # Reviso que tenga permiso
    if 'ciclo_lectivo_update' not in session['permisos']:
        flash('No tiene permiso para agregar un taller al ciclo lectivo' )
        return redirect('/home') 

    Taller.db = get_db()
    id_ciclo = request.args.get('ciclo', None)
    id_taller = request.args.get('taller', None)
    if not Taller.existe_taller_en_ciclo_lectivo(id_ciclo, id_taller):
        if Taller.insertar_taller_en_ciclo_lectivo(id_ciclo, id_taller):
            flash("El taller ha sido insertado correctamente")
    else:
        flash('El taller ya ha sido insertado en el ciclo lectivo!' ) 
        print (Taller.existe_taller_en_ciclo_lectivo(id_ciclo, id_taller))

    return redirect('/index/ciclo_lectivo')