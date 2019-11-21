from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Ciclo_lectivo import Ciclo_lectivo
from flaskps.models.Docente import Docente
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.models.Informacion import Informacion
from flaskps.helpers.auth import authenticated
from flaskps.helpers.apiReferencias import tipos_documento, localidades
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import SignUpCicloLectivoForm, BusquedaCicloLectivoForm, EditarCicloLectivoForm
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

    # Obtengo los talleres de los ciclos lectivos
    talleres = []
    for t in range(len(Ciclo_lectivo.get_ciclos_lectivos()) + 1):
        taller = Ciclo_lectivo.get_taller(t)
        talleres.append(taller)
        
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
                            error_busqueda=error_busqueda,
                            talleres=talleres)
    
# REGISTRAR CICLO LECTIVO

@mod.route("/ciclo_lectivo/registrar", methods=['GET', 'POST'])
def registrar():
    
    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para registrar ciclos lectivos.')
        return redirect('/home')  
       
    
    Usuario.db = get_db()
    form = SignUpCicloLectivoForm()
    
    # Armo la lista de opciones del select
    talleres = [('0', 'Seleccionar taller')]
    for t in Ciclo_lectivo.all_talleres():
        talleres.append( (t['nombre'], t['nombre']) )
    form.taller.choices = talleres

    # para manejar los mensajes flash
    error=0
    exito=0
    
    if request.method == 'POST':
        
        if form.validate_on_submit():
            
            Ciclo_lectivo.db = get_db()

            ciclo_lectivo = Ciclo_lectivo(form.fecha_ini.data, form.fecha_fin.data, form.semestre.data)

            if not Ciclo_lectivo.existe(Ciclo_lectivo, form.taller.data):
                  
                Ciclo_lectivo.insert(ciclo_lectivo)
                
                # chequeo si se otorgó taller y lo agrego
                if form.taller.data != '0':
                    ciclo_lectivo.agregar_taller(ciclo_lectivo, form.taller.data)
                
                flash("Ciclo lectivo registrado correctamente.")
                exito = 1
                
            else:
                flash("Error al registrar: Ya existe ese ciclo lectivo.")
                error = 1
                
        else: 
            flash("Debe completar todos los campos")
            error = 1
            
    return render_template("ciclos_lectivos/registrar.html", form=form, error=error, exito=exito)
    
# ELIMINAR CICLO LECTIVO

@mod.route("/ciclo_lectivo/eliminar/<id_ciclo_lectivo>")
def eliminar(id_ciclo_lectivo):

    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para eliminar ciclos lectivos')
        return redirect('/index/ciclo_lectivo')
   
    Ciclo_lectivo.db = get_db()
    if Ciclo_lectivo.eliminar(id_ciclo_lectivo):
        flash('El ciclo lectivo se eliminó con éxito')
    
    return redirect('/index/ciclo_lectivo')

#  EDITAR CICLO LECTIVO
@mod.route("/ciclo_lectivo/editar/<id_ciclo_lectivo>", methods=['GET', 'POST'])
def editar(id_ciclo_lectivo):

    # Reviso que tenga permiso
    if 'ciclo_lectivo_update' not in session['permisos']:
        flash('No tiene permiso para editar ciclos lectivos. ')
        return redirect('/home')  
    else:  
    

        form = EditarCicloLectivoForm()
        # para manejar los mensajes flash
        error=0
        exito=0
        Ciclo_lectivo.db = get_db()
        ciclo_lectivo = Ciclo_lectivo.get_ciclo_lectivo(id_ciclo_lectivo)
        taller = Ciclo_lectivo.get_taller(id_ciclo_lectivo)

        if ciclo_lectivo:
            
            if request.method == 'POST':

                if form.validate_on_submit():

                    Ciclo_lectivo.editar(id_ciclo_lectivo, form.fecha_ini.data, form.fecha_fin.data, form.semestre.data)

                    # vuelvo a consultar por los valores del ciclo lectivo
                    ciclo_lectivo = Ciclo_lectivo.get_ciclo_lectivo(id_ciclo_lectivo)    
                    flash("Ciclo lectivo editado correctamente.")
                    exito = 1
                else:
                    flash("Debe completar todos los campos")
                    error = 1
            
           
            # vuelvo a setear el form con los valores actualizados del ciclo lectivo

            form.process() #IMPORTANTE

            form.fecha_ini.data = ciclo_lectivo['fecha_ini']
            form.fecha_fin.data = ciclo_lectivo['fecha_fin']
            form.semestre.data = ciclo_lectivo['semestre']
            form.taller.data = taller


            return render_template("ciclos_lectivos/editar.html", form=form, error=error, exito=exito)
        else:
            return redirect("/home")


# SHOW CICLO LECTIVO
@mod.route("/ciclo_lectivo/show/<id_ciclo_lectivo>")
def show(id_ciclo_lectivo):
    
    # Reviso que tenga permiso
    if 'ciclo_lectivo_show' in session['permisos']:

        Ciclo_lectivo.db = get_db()
        ciclo_lectivo = Ciclo_lectivo.get_ciclo_lectivo(id_ciclo_lectivo)

        if (ciclo_lectivo):
            # Obtengo el taller del ciclo lectivo
            taller = Ciclo_lectivo.get_taller(id_ciclo_lectivo)

            # Obtengo los estudiantes del ciclo lectivo
            estudiantes = []
            for e in Ciclo_lectivo.get_estudiantes(ciclo_lectivo['id']):
                estudiantes.append(e['nombre'])

            # Obtengo los estudiantes del ciclo lectivo
            docentes = []
            for d in Ciclo_lectivo.get_docentes(ciclo_lectivo['id']):
                docentes.append(d['nombre'])      

            return render_template("ciclos_lectivos/show.html", ciclo_lectivo=ciclo_lectivo, taller=taller, estudiantes=estudiantes, docentes=docentes)
        else:
            return redirect("/home")

    else:
        flash("No tiene permisos para realizar ésta acción")
        return redirect("/home")