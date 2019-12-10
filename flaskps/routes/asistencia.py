from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Asistencia import Asistencia
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible 
from flaskps.forms import BusquedaAsistenciaForm
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
        print(total)
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
                            error_busqueda=error_busqueda)
