from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.forms import SignUpForm
from flask_paginate import Pagination, get_page_parameter


mod = Blueprint('usuario', __name__)

# LISTADOS
@mod.route("/index/<rol>")
def index(rol):
    # Setear variables
    Configuracion.db = get_db()
    per_page = Configuracion.get_paginacion()['paginacion']
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    Usuario.db = get_db()
    
    # Total registros
    total = Usuario.get_usuarios_por_rol(rol)
    total = len(total)

    # Consulta usando offset y limit
    usuarios = Usuario.get_usuarios_por_rol_paginados(rol, per_page, offset)

    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total, 
                            record_name='usuarios',
                            css_framework='bootstrap4')
    
    # Setear el titulo
    titulo = get_titulo(rol)
    
    return render_template('usuarios/index.html', 
                            pagination=pagination, 
                            usuarios=usuarios, 
                            rol=rol,
                            titulo=titulo)


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



# ------------------------------------------------
def get_titulo(rol):
    switcher = {
        'estudiante': "Estudiantes",
        'docente': "Docentes",
        'preceptor': "Preceptores",
        'admin': "Administradores"
    }
    return switcher.get(rol, "Rol invalido")
