from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Estudiante import Estudiante
from flaskps.helpers.auth import authenticated


mod = Blueprint('estudiante', __name__)

@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")