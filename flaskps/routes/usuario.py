from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Estudiante import Estudiante
from flaskps.models.Configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.forms import SignUpForm, SignUpEstudianteForm, BusquedaUsuarioForm, EditarForm
from flask_paginate import Pagination, get_page_parameter


mod = Blueprint('usuario', __name__)


@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")

# LISTADOS
@mod.route("/index/usuarios")
def index():

    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para administrar usuarios.')
        return redirect('/home') 

    Usuario.db = get_db()
    form = BusquedaUsuarioForm()
    
    # Armo la lista de opciones del select
    roles = [('0', 'Seleccionar rol')]
    for r in Usuario.all_roles():
        roles.append( (r['nombre'], r['nombre']) )
    form.rol.choices = roles
    
    error_busqueda = 0

    search = False
    rol = request.args.get('rol')
    termino = request.args.get('termino')
    busqueda_activos = request.args.get('activos')
    busqueda_inactivos = request.args.get('inactivos')
    
    if termino or busqueda_activos or busqueda_inactivos or rol:
        search = True

    # seteo el value del input si vino con algo
    form.rol.data = rol
    form.termino.data = termino
    form.activos.data = busqueda_activos
    form.inactivos.data = busqueda_inactivos
    
    # Setear variables de paginacion
    Configuracion.db = get_db()
    per_page = Configuracion.get_paginacion()['paginacion']
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    
    
    if search:
        # Total registros
        total = Usuario.get_usuarios(rol, termino, busqueda_activos, busqueda_inactivos)
        # Consulta usando offset y limit
        usuarios = Usuario.get_usuarios_paginados(per_page, offset, rol, termino, busqueda_activos, busqueda_inactivos)
    else:
        # Total registros
        total = Usuario.get_usuarios()
        # Consulta usando offset y limit
        usuarios = Usuario.get_usuarios_paginados(per_page, offset)
    
    total = len(total)
    if (total == 0 and search == True):
        flash("La búsqueda no obtuvo resultados.")
        error_busqueda = 1
        
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            search=search,
                            found=total,
                            record_name='usuarios',
                            css_framework='bootstrap4')
    
    return render_template('usuarios/index.html', 
                            pagination=pagination, 
                            usuarios=usuarios, 
                            form=form, 
                            error_busqueda=error_busqueda)




# REGISTRAR USUARIO
@mod.route("/registrar", methods=['GET', 'POST'])
def registrar():
    
    # Reviso que tenga permiso
    if not Usuario.tengo_permiso_registrar(session['permisos']):
        flash('No tiene permiso para registrar usuarios. ')
        return redirect('/home')  
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
                    
                    flash("Usuario registrado correctamente.")
                    exito = 1
                    
                else:
                    flash("Error al registrar: Ya existe ese nombre de usuario.")
                    error = 1
                    
            else: 
                flash("Debe completar todos los campos y el email ingresado debe ser válido.")
                error = 1
                
                
        # para mostrar los checkbox según los roles que puedo agregar
        puedo_docente = Usuario.tengo_permiso( session['permisos'], 'docente_new')
        puedo_preceptor = Usuario.tengo_permiso(session['permisos'], 'preceptor_new')
        puedo_admin = Usuario.tengo_permiso(session['permisos'], 'admin_new')

                
        return render_template("usuarios/registrar.html", form=form, error=error, exito=exito, puedo_admin=puedo_admin, puedo_docente=puedo_docente, puedo_preceptor=puedo_preceptor)


#  ACTIVAR/DESACTIVAR USUARIO
@mod.route("/activar/<id_usuario>")
def activar(id_usuario):
    
    if int(id_usuario) == session['user']['id']:
        flash('No se puede modificar a sí mismo!')
        return redirect('/index/usuarios')
    
    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para activar / desactivar usuarios')
        return redirect('/index/usuarios')

    Usuario.db = get_db()
    Usuario.activar(id_usuario)
    
    flash("Se guardaron los cambios con éxito")
    return redirect("/index/usuarios")


#  EDITAR USUARIO
@mod.route("/editar/<id_usuario>", methods=['GET', 'POST'])
def editar(id_usuario):
    
    if int(id_usuario) == session['user']['id']:
        flash('No se puede modificar a sí mismo!')
        return redirect('/index/usuarios')

    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para editar usuarios')
        return redirect('/index/usuarios')
    

    form = EditarForm()
    # para manejar los mensajes flash
    error=0
    exito=0
    Usuario.db = get_db()
    usuario = Usuario.get_user(id_usuario)
    
    if request.method == 'POST':
        
        if form.validate_on_submit():          

            Usuario.editar(id_usuario, form.email.data,form.username.data, form.first_name.data, form.last_name.data)
            usuario = Usuario(usuario['email'], usuario['username'], usuario['password'], usuario['first_name'], usuario['last_name'])
            # chequeo qué permisos se le otorgaron al usuario        
            if (form.es_admin.data):
                usuario.agregar_rol('admin', usuario)
            else:
                usuario.quitar_rol('admin', usuario)    
            
            if (form.es_preceptor.data):
                usuario.agregar_rol('preceptor', usuario)
            else:
                usuario.quitar_rol('preceptor', usuario)

            if (form.es_docente.data):
                usuario.agregar_rol('docente', usuario)
            else:
                usuario.quitar_rol('docente', usuario)   

            # vuelvo a consultar por los valores del usuario
            usuario = Usuario.get_user(id_usuario)    
            flash("Usuario editado correctamente.")
            exito = 1
                
        else: 
            flash("Debe completar todos los campos.")
            error = 1
            
    # vuelvo a setear el form con los valores actualizados del usuario
    form.email.data = usuario['email']
    form.username.data = usuario['username']
    form.first_name.data = usuario['first_name']
    form.last_name.data = usuario['last_name']
   
    # obtengo roles del usuario y seteo los checkbox
    tuplas_roles = Usuario.get_roles(usuario['id'])
    roles = []
    for t in tuplas_roles:
        roles.append(t['nombre'])
    if 'admin' in roles:
        form.es_admin.data = 1
    if 'preceptor' in roles:
        form.es_preceptor.data = 1
    if 'docente' in roles:
        form.es_docente.data = 1


    return render_template("usuarios/editar.html", form=form, error=error, exito=exito)


# ELIMINAR USUARIO

@mod.route("/eliminar/<id_usuario>/<rol>")
def eliminar(id_usuario, rol):
    
    if int(id_usuario) == session['user']['id']:
        flash('No se puede eliminar a sí mismo!')
        return redirect('/index/' + rol)

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

# SHOW USUARIO

@mod.route("/show/<id_usuario>/<rol>")
def show(id_usuario, rol):
    
    # Reviso que tenga permiso
    permiso = rol+'_show'
    if not Usuario.tengo_permiso(session['permisos'], permiso) and int(id_usuario) != session['user']['id']:
        flash('No tiene permiso para ver el detalle de éste tipo de usuario')
        return redirect('/index/' + rol)

    else:
        Usuario.db = get_db()
        usuario = Usuario.get_user(id_usuario)       
        
        # obtengo roles del usuario y seteo los checkbox
        tuplas_roles = Usuario.get_roles(usuario['id'])
        roles = []
        for t in tuplas_roles:
            roles.append(t['nombre'])

        return render_template("usuarios/show.html", usuario=usuario, roles=roles)


# ------------------------------------------------
def get_titulo(rol):
    switcher = {
        'estudiante': "Estudiantes",
        'docente': "Docentes",
        'preceptor': "Preceptores",
        'admin': "Administradores"
    }
    return switcher.get(rol, "Rol invalido")
