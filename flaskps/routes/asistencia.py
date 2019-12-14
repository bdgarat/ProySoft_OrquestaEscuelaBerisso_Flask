from flask import Blueprint
from flaskps.db import get_db
from datetime import date
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Asistencia import Asistencia
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible 
from flaskps.forms import BusquedaAsistenciaForm, PasarAsistenciaForm
from flask_paginate import Pagination, get_page_parameter


mod = Blueprint('asistencia', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")

@mod.route("/asistencia/index")
def asistencia():
    form = BusquedaAsistenciaForm()
    
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

    Asistencia.db = get_db()
    
    if search:
        # Total registros
        total = Asistencia.get_talleres_con_profesor(termino)
        # Consulta usando offset y limit
        talleres = Asistencia.get_talleres_con_profesor_paginados(per_page, offset, termino)
    else:
        # Total registros
        total = Asistencia.get_talleres_con_profesor(termino)
        # Consulta usando offset y limit
        talleres = Asistencia.get_talleres_con_profesor_paginados(per_page, offset, termino)

    total = len(total)
    if (total == 0 and search == True):
        flash("La búsqueda no obtuvo resultados.")
        error_busqueda = 1


    # form.ciclo_lectivo.data = ciclo
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            search=search,
                            found=total,
                            record_name='Talleres',
                            css_framework='bootstrap4')
    
    return render_template('asistencia/index.html', 
                            pagination=pagination, 
                            talleres=talleres,
                            form=form, 
                            error_busqueda=error_busqueda, )
    
    
@mod.route("/asistencia/pasar/<ciclo>/<taller>", methods=['GET', 'POST'])
def pasar(ciclo, taller):
    
    # Reviso que tenga permiso
    if 'asistencia' not in session['permisos']:
        flash('No tiene permiso para pasar asistencia' )
        return redirect('/home')
    
    Asistencia.db = get_db()
    alumnos = Asistencia.get_alumnos_por_taller_y_ciclo(ciclo, taller)
        
    form = PasarAsistenciaForm()
    estados = []
    estados.append((1, 'PRESENTE'))
    estados.append((2, 'AUSENTE'))
    form.estado.choices = estados
    
    # para manejar los mensajes flash
    error=0
    exito=0
    
    
    if request.method == 'POST':
        
        form.estado.data = int(form.estado.data)
            
        if form.validate_on_submit():

            if Asistencia.existe(ciclo, taller, form.id.data, date.today(), form.estado.data):
                
                error = 1
                flash("Ya se registró el asistencia para ese alumno.")
            else:
                if Asistencia.hay_que_actualizar(ciclo, taller, form.id.data, date.today(), form.estado.data):
                    
                    Asistencia.actualizar(ciclo, taller, form.id.data, date.today(), form.estado.data)
                    exito = 1
                    flash("Se actualizó la asistencia para ese alumno.")
                else:
                    exito = Asistencia.pasar(ciclo, taller, form.id.data, date.today(), form.estado.data)
                    if exito:
                        flash("Asistencia registrada correctamente.")
            
    # alumnos que ya tienen cargado asistencia para el taller, ciclo y dia
    alumnos_con_asistencia = Asistencia.get_alumnos_con_asistencia(ciclo, taller, date.today())
    
    return render_template('asistencia/pasar.html', form=form, alumnos=alumnos, error=error, exito=exito, alumnos_con_asistencia=alumnos_con_asistencia)
