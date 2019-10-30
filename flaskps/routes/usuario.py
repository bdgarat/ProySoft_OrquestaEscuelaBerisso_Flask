from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.forms import SignUpForm, BusquedaForm, EditarForm
from flask_paginate import Pagination, get_page_parameter


mod = Blueprint('usuario', __name__)


@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")

# LISTADOS
@mod.route("/index/<rol>")
def index(rol):

    # Reviso que tenga permiso
    permiso = rol+'_index'
    if not Usuario.tengo_permiso(session['permisos'], permiso):
        flash('No tiene permiso para visualizar el listado de ' + get_titulo(rol) )
        return redirect('/home')    

    form = BusquedaForm()

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

    Usuario.db = get_db()
    
    if search:
        # Total registros
        total = Usuario.get_usuarios_por_rol(rol, termino)
        # Consulta usando offset y limit
        usuarios = Usuario.get_usuarios_por_rol_paginados(rol, per_page, offset, termino)
    else:
        # Total registros
        total = Usuario.get_usuarios_por_rol(rol)
        # Consulta usando offset y limit
        usuarios = Usuario.get_usuarios_por_rol_paginados(rol, per_page, offset)

    total = len(total)
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            search=search,
                            found=total,
                            record_name='usuarios',
                            css_framework='bootstrap4')
    
    # Setear el titulo
    titulo = get_titulo(rol)
    
    return render_template('usuarios/index.html', 
                            pagination=pagination, 
                            usuarios=usuarios, 
                            rol=rol,
                            titulo=titulo,
                            form=form)


@mod.route("/registrar", methods=['GET', 'POST'])
def registrar():
    
    # Reviso que tenga permiso
    if not Usuario.tengo_permiso_registrar(session['permisos']):
        flash("Usted no tiene permiso para realizar esta operacón")
        return redirect("/home")
    else:     
    
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
                
                
        # para mostrar los checkbox según los roles que puedo agregar
        puedo_estudiante = Usuario.tengo_permiso(session['permisos'], 'estudiante_new')
        puedo_docente = Usuario.tengo_permiso( session['permisos'], 'docente_new')
        puedo_preceptor = Usuario.tengo_permiso(session['permisos'], 'preceptor_new')
        puedo_admin = Usuario.tengo_permiso(session['permisos'], 'admin_new')

                
        return render_template("usuarios/registrar.html", form=form, error=error, exito=exito, puedo_admin=puedo_admin, puedo_docente=puedo_docente, puedo_estudiante=puedo_estudiante, puedo_preceptor=puedo_preceptor)


#  ACTIVAR/DESACTIVAR USUARIO

@mod.route("/activar/<id_usuario>/<rol>")
def activar(id_usuario, rol):
    
    # Reviso que tenga permiso
    permiso = rol+'_update'
    if not Usuario.tengo_permiso(session['permisos'], permiso):
        flash('No tiene permiso para actualizar este tipo de usuario')
        return redirect('/index/' + rol)

    Usuario.db = get_db()
    Usuario.activar(id_usuario)
    
    flash("Se guardaron los cambios con éxito")
    return redirect("/index/"+rol)

#  EDITAR USUARIO


@mod.route("/editar/<id_usuario>/<rol>", methods=['GET', 'POST'])
def editar(id_usuario, rol):
    
    # Reviso que tenga permiso
    permiso = rol+'_update'
    if not Usuario.tengo_permiso(session['permisos'], permiso):
        flash('No tiene permiso para actualizar este tipo de usuario')
        return redirect('/index/' + rol)
    

    form = EditarForm()
    # para manejar los mensajes flash
    error=0
    exito=0
    Usuario.db = get_db()
    usuario = Usuario.get_user(id_usuario)
    
    if request.method == 'POST':
        
        if form.validate_on_submit():          
                
            ok = Usuario.editar(id_usuario, form.email.data,form.username.data, form.first_name.data, form.last_name.data)
            print(ok)
            
            flash("Usuario editado correctamente.")
            exito = 1
                
        else: 
            flash("Debe completar todos los campos.")
            error = 1
            
    usuario = Usuario.get_user(id_usuario)
    
    # vuelvo a setear el form con los valores actualizados del usuario
    form.email.data = usuario['email']
    form.username.data = usuario['username']
    form.first_name.data = usuario['first_name']
    form.last_name.data = usuario['last_name']
                
    return render_template("usuarios/editar.html", form=form, error=error, exito=exito)


# ELIMINAR USUARIO

@mod.route("/eliminar/<id_usuario>/<rol>")
def eliminar(id_usuario, rol):
    
    # Reviso que tenga permiso
    permiso = rol+'_destroy'
    if not Usuario.tengo_permiso(session['permisos'], permiso):
        flash('No tiene permiso para eliminar este tipo de usuario')
        
    else:
        Usuario.db = get_db()
        ok = Usuario.eliminar(id_usuario)
        print(ok)
        flash('El usuario se eliminó con éxito')
    
    return redirect('/index/' + rol)


# ------------------------------------------------
def get_titulo(rol):
    switcher = {
        'estudiante': "Estudiantes",
        'docente': "Docentes",
        'preceptor': "Preceptores",
        'admin': "Administradores"
    }
    return switcher.get(rol, "Rol invalido")
