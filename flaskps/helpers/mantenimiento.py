from flask import session
from flaskps.models.Configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.db import get_db

def sitio_disponible():
    # Reviso el estado del sitio
    Configuracion.db = get_db()
    habilitado = Configuracion.get_sitio_habilitado()['sitio_habilitado']
    if habilitado == 0:
        if not authenticated(session) or (authenticated(session) and 'admin' not in session['roles']):
            return False
    return True