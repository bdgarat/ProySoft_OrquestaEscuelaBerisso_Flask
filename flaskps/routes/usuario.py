from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Config import Config
from flaskps.helpers.auth import authenticated
from flaskps.forms import SignUpForm, ConfigForm


mod = Blueprint('usuario', __name__)


# LISTADOS
@mod.route("/index/<rol>")
def index(rol):

    Usuario.db = get_db()
    usuarios = Usuario.get_usuarios_por_rol(rol)

    return render_template('usuarios/index.html', usuarios=usuarios)


@mod.route("/registrar", methods=['GET', 'POST'])
def registrar():
    form = SignUpForm()

    if form.validate_on_submit():
        Usuario.db = get_db()
        
        if not Usuario.existe(form.username.data):
            
            usuario = Usuario(form.email.data, form.username.data, form.password.data, form.first_name.data, form.last_name.data)
            ok = Usuario.insert(usuario)
            
            if not ok:
                flash("No se puede registrar al usuario.")
                return redirect("/insertar")  
            
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
            
        else:
            flash("Error al registrar: Ya existe ese nombre de usuario.")
            
    flash("Debe completar todos los campos.")
    return render_template("usuarios/registrar.html", form=form)

@mod.route("/config", methods=['GET', 'POST'])
def config():
    form = ConfigForm()
    Usuario.db = get_db()   
    config_actual = Usuario.get_config()
    
    # Problema: el formulario solo pasa la validacion si escribo algo en el campo 'paginacion', si lo dejo vacio no pasa

    if form.validate_on_submit():
        Usuario.set_config( Config( form.titulo.data, form.descripcion.data, form.contacto.data, form.paginacion.data, form.sitio_habilitado.data) )
        flash("Se actualizó la información con éxito")
    else:
        flash("Debe completar el campo 'paginación' con un valor numérico")

        
        
    return render_template("usuarios/config.html", form=form, config=config_actual)
