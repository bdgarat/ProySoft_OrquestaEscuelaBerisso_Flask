from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible


mod = Blueprint('nucleo', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")


# Mapa
@mod.route("/nucleo/mapa")
def mapa():
    return render_template('nucleos/mapa.html')