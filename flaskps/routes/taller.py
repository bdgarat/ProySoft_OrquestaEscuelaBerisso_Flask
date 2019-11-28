from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Docente import Docente
from flaskps.models.Configuracion import Configuracion
from flaskps.models.Usuario import Usuario
from flaskps.models.Informacion import Informacion
from flaskps.models.Taller import Taller
from flaskps.helpers.auth import authenticated
from flaskps.helpers.apiReferencias import tipos_documento, localidades
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import BusquedaTallerForm
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
def index_docente():

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
        
    insertar_taller = False
    if (request.args.get('ciclo', None)):
        insertar_taller = True

    ciclo = request.args.get('ciclo', None)


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
                            ciclo=ciclo)