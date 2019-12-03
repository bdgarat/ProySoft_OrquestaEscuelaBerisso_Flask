from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Docente import Docente
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.models.Informacion import Informacion
from flaskps.models.Taller import Taller
from flaskps.models.Ciclo_lectivo import Ciclo_lectivo
from flaskps.helpers.auth import authenticated
from flaskps.helpers.apiReferencias import tipos_documento, localidades
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import BusquedaTallerForm, AsignarHorarioTallerForm
from flask_paginate import Pagination, get_page_parameter



mod = Blueprint('taller', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")
    
    
# LISTADOS
@mod.route("/index/taller")
def index_taller():

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
        total = Taller.get_talleres(termino)
        # Consulta usando offset y limit
        talleres = Taller.get_talleres_paginados(per_page, offset, termino)
    else:
        # Total registros
        total = Taller.get_talleres()
        # Consulta usando offset y limit
        talleres = Taller.get_talleres_paginados(per_page, offset, termino)

    total = len(total)
    if (total == 0 and search == True):
        flash("La búsqueda no obtuvo resultados.")
        error_busqueda = 1
        
    ciclo = request.args.get('ciclo', None)
    talleres_inscriptos = None
    insertar_taller = False
    if ciclo and (ciclo != 'None' and ciclo != ''):
        insertar_taller = True
        talleres_inscriptos = Taller.talleres_ciclo(ciclo)


    # form.ciclo_lectivo.data = ciclo
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            search=search,
                            found=total,
                            record_name='Talleres',
                            css_framework='bootstrap4')
    
    return render_template('talleres/index.html', 
                            pagination=pagination, 
                            talleres=talleres,
                            form=form, 
                            error_busqueda=error_busqueda,
                            insertar_taller=insertar_taller,
                            talleres_inscriptos=talleres_inscriptos,
                            ciclo=ciclo)

# SHOW
@mod.route("/taller/show/<id_taller>")
def show_taller(id_taller):
     # Reviso que tenga permiso
    if 'taller_show' not in session['permisos']:
        flash('No tiene permiso para visualizar un taller en un ciclo lectivo' )
        return redirect('/home')
    id_ciclo = request.args.get('ciclo', None)
    Taller.db = get_db()
    taller = Taller.get_taller_show(id_taller, id_ciclo)
    estudiantes = Taller.get_estudiantes_show(id_taller, id_ciclo)
    docentes = Taller.get_docentes_show(id_taller, id_ciclo)

    print(taller)
    print(estudiantes)
    print(docentes)
    return render_template('talleres/show.html', taller=taller, estudiantes=estudiantes, docentes=docentes)

# ASIGNAR HORARIO
@mod.route("/taller/asignar_horario/<id_ciclo>/<id_taller>", methods=['GET', 'POST'] )
def asignar_horario(id_ciclo, id_taller):
    
    if 'taller_update' not in session['permisos']:
        flash('No tiene permiso para editar un taller en un ciclo lectivo' )
        return redirect('/home')
    
    
    Taller.db = get_db()
    Ciclo_lectivo.db = get_db()
    Informacion.db = get_db()
    
    if (len(Taller.tiene_docente(id_ciclo, id_taller)) == 0):
        flash('No se puede realizar ésta acción porque el taller no tiene asignado ningún docente' )
        return redirect('/home')
    
    form = AsignarHorarioTallerForm()
    exito = 0
    error = 0
    
    taller = Taller.get_taller(id_taller)
    ciclo = Ciclo_lectivo.get_ciclo_lectivo(id_ciclo)
    
    form.profesor.choices = Taller.get_docentes_ciclo_taller(ciclo['id'], taller[0]['id'])
    form.nucleo.choices = Informacion.all('nucleo')
    
    form.dia.choices = [(1, 'LUNES'), (2, 'MARTES'), (3, 'MIERCOLES'), (4, 'JUEVES'), (5, 'VIERNES'), (6, 'SABADO'), (7, 'DOMINGO')]
        
    if request.method == 'POST':
        
        form.profesor.data = int(form.profesor.data)
        form.nucleo.data = int(form.nucleo.data)
        form.dia.data = int(form.dia.data)

        if form.validate_on_submit():
            
            # chequeo que haya ingresado bien los horarios
            if form.hora_inicio.data < form.hora_fin.data:
                
                if not Taller.existe_horario(ciclo['id'], taller[0]['id'], form.profesor.data, form.nucleo.data, form.hora_inicio.data, form.hora_fin.data, form.dia.data):
                    Taller.agregar_horario(ciclo['id'], taller[0]['id'], form.profesor.data, form.nucleo.data, form.hora_inicio.data, form.hora_fin.data, form.dia.data)
                    exito=1
                    flash("Se agregó el horario correctamente.")
                else:
                    flash("Ya existe un horario asignado para el taller, docente, nucleo, dia y horario seleccionados.")
                    error = 1
                
            else:
                flash("La hora de inicio del taller debe ser menor a la hora de fin del mismo.")
                error = 1
        else:
            flash("Debe completar todos los campos.")
            error = 1
        
    return render_template('talleres/asignar_horario.html', taller = taller, ciclo = ciclo, form = form, exito=exito, error=error)