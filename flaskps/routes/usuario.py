from flask import Blueprint
from flaskps.db import get_db
from flask import render_template, flash, redirect, session, abort, request
from flaskps.models.Usuario import Usuario
from flaskps.models.Estudiante import Estudiante
from flaskps.models.Configuracion import Configuracion
from flaskps.helpers.auth import authenticated
from flaskps.helpers.mantenimiento import sitio_disponible
from flaskps.forms import SignUpForm, SignUpEstudianteForm, BusquedaUsuarioForm, EditarForm
from flask_paginate import Pagination, get_page_parameter

mod = Blueprint('usuario', __name__)


@mod.before_request
def before_request():
    if not authenticated(session):
        return redirect("/home")
    # Reviso el estado del sitio
    if not sitio_disponible():
        return redirect("/logout")

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
@mod.route("/usuario/registrar", methods=['GET', 'POST'])
def registrar():
    
    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para registrar usuarios.')
        return redirect('/home')  
       
    
    Usuario.db = get_db()
    form = SignUpForm()
    
    # Armo la lista de opciones del select
    roles = [('0', 'Seleccionar rol')]
    for r in Usuario.all_roles():
        roles.append( (r['nombre'], r['nombre']) )
    form.rol.choices = roles

    # para manejar los mensajes flash
    error=0
    exito=0
    
    if request.method == 'POST':
        
        if form.validate_on_submit():
            
            Usuario.db = get_db()
            
            if not Usuario.existe(form.username.data):
                  
                usuario = Usuario(form.email.data, form.username.data, form.password.data, form.first_name.data, form.last_name.data)
                Usuario.insert(usuario)
                
                # chequeo si se otorgó rol y lo agrego
                if form.rol.data != '0':
                    usuario.agregar_rol(form.rol.data, usuario)
                
                flash("Usuario registrado correctamente.")
                exito = 1
                
            else:
                flash("Error al registrar: Ya existe ese nombre de usuario.")
                error = 1
                
        else: 
            flash("Debe completar todos los campos y el email ingresado debe ser válido.")
            error = 1
            
    return render_template("usuarios/registrar.html", form=form, error=error, exito=exito)


#  ACTIVAR/DESACTIVAR USUARIO
@mod.route("/usuario/activar/<id_usuario>")
def activar(id_usuario):
    
    if int(id_usuario) == session['user']['id']:
        flash('No se puede modificar a sí mismo!')
        return redirect('/index/usuarios')
    
    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para activar / desactivar usuarios')
        return redirect('/index/usuarios')

    Usuario.db = get_db()
    if Usuario.activar(id_usuario):
        flash("Se guardaron los cambios con éxito")
    
    return redirect("/index/usuarios")


#  EDITAR USUARIO
@mod.route("/usuario/editar/<id_usuario>", methods=['GET', 'POST'])
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
    
    if usuario:

        if request.method == 'POST':
                
            Usuario.editar(id_usuario, form.email.data,form.username.data, form.first_name.data, form.last_name.data)
            usuario = Usuario(usuario['email'], usuario['username'], usuario['password'], usuario['first_name'], usuario['last_name'])
                
            # chequeo si se otorgó rol y lo agrego
            if form.agregar_rol.data != '0':
                usuario.agregar_rol(form.agregar_rol.data, usuario)

            # chequeo si se quitó rol y lo quito
            if form.quitar_rol.data != '0':
                usuario.quitar_rol(form.quitar_rol.data, usuario)

            # vuelvo a consultar por los valores del usuario
            usuario = Usuario.get_user(id_usuario)    
            flash("Usuario editado correctamente.")
            exito = 1
                    
                
        # vuelvo a setear el form con los valores actualizados del usuario
        form.email.data = usuario['email']
        form.username.data = usuario['username']
        form.first_name.data = usuario['first_name']
        form.last_name.data = usuario['last_name']
    
        # obtengo roles del usuario
        roles_usuario = []
        for t in Usuario.get_roles(usuario['id']):
            roles_usuario.append(t['nombre'])

        # Armo la lista de opciones del select para agregar
        agregar_roles = [('0', 'Seleccionar')]
        for r in Usuario.all_roles():
            if r['nombre'] not in roles_usuario:
                agregar_roles.append( (r['nombre'], r['nombre']) )

        # Armo la lista de opciones del select para eliminar
        quitar_roles = [('0', 'Seleccionar')]
        for r in Usuario.all_roles():
            if r['nombre'] in roles_usuario:
                quitar_roles.append( (r['nombre'], r['nombre']) )
        

        form.agregar_rol.choices = agregar_roles
        form.quitar_rol.choices = quitar_roles

        return render_template("usuarios/editar.html", form=form, roles_usuario=roles_usuario, error=error, exito=exito)
    else:
        return redirect("/home")


# ELIMINAR USUARIO

@mod.route("/usuario/eliminar/<id_usuario>")
def eliminar(id_usuario):
    
    if int(id_usuario) == session['user']['id']:
        flash('No se puede eliminar a sí mismo!')
        return redirect('/index/usuarios')

    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para eliminar usuarios')
        return redirect('/index/usuarios')
   
    Usuario.db = get_db()
    if Usuario.eliminar(id_usuario):
        flash('El usuario se eliminó con éxito')
    
    return redirect('/index/usuarios')


# SHOW USUARIO
@mod.route("/usuario/show/<id_usuario>")
def show(id_usuario):
    
    # Reviso que tenga permiso
    if 'admin' not in session['roles']:
        flash('No tiene permiso para ver usuarios')
        return redirect('/index/usuarios')

    Usuario.db = get_db()
    usuario = Usuario.get_user(id_usuario) 
    print(usuario)   
    
    if usuario:     
        # obtengo roles del usuario
        roles = []
        for t in Usuario.get_roles(usuario['id']):
            roles.append(t['nombre'])

        return render_template("usuarios/show.html", usuario=usuario, roles=roles)
    else:
        return redirect("/home")


# ------------------------------------------------
def get_titulo(rol):
    switcher = {
        'estudiante': "Estudiantes",
        'docente': "Docentes",
        'preceptor': "Preceptores",
        'admin': "Administradores"
    }
    return switcher.get(rol, "Rol invalido")
