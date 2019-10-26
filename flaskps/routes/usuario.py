from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.forms import SignUpForm


mod = Blueprint('usuario', __name__)


# LISTADOS
@mod.route("/index/<rol>")
def index(rol):

    Usuario.db = get_db()
    usuarios = Usuario.get_usuarios_por_rol(rol)

    return render_template('usuarios/index.html', usuarios=usuarios, rol=rol)


@mod.route("/registrar", methods=['GET', 'POST'])
def registrar():
    form = SignUpForm()
    # para manejar los mensajes flash
    error=0
    exito=0
    
    if request.method == 'POST':
        

        if form.validate_on_submit():
            Usuario.db = get_db()
            
            if not Usuario.existe(form.username.data):
                
                usuario = Usuario(form.email.data, form.username.data, form.password.data, form.first_name.data, form.last_name.data)
                Usuario.insert(usuario)
                
                # chequeo qué permisos se le otorgaron al usuario
                
                if (form.es_admin.data):
                    usuario.agregar_rol('admin', usuario)
                    
                if (form.es_preceptor.data):
                    usuario.agregar_rol('preceptor', usuario)
                    
                if (form.es_docente.data):
                    usuario.agregar_rol('docente', usuario)
                    
                if (form.es_estudiante.data):
                    usuario.agregar_rol('estudiante', usuario)
                
                flash("Usuario registrado correctamente.")
                exito = 1
                
            else:
                flash("Error al registrar: Ya existe ese nombre de usuario.")
                error = 1
                
        else: 
            flash("Debe completar todos los campos.")
            error = 1
            
    return render_template("usuarios/registrar.html", form=form, error=error, exito=exito)


@mod.route("/activar/<id_usuario>/<rol>")
def activar(id_usuario, rol):
    
    Usuario.db = get_db()
    Usuario.activar(id_usuario)
    
    flash("Se guardaron los cambios con éxito")
    return redirect("/index/"+rol)