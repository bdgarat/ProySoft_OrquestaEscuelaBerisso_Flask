from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField, DateField, TimeField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Contraseña', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Iniciar sesión', render_kw={"class": "btn btn-lg btn-primary btn-block"})
    
class ConfigForm(FlaskForm):   
    titulo = StringField('Titulo del sitio', render_kw={"class": "form-control"})
    descripcion = TextAreaField('Descripcion', render_kw={"class": "form-control"})   
    contacto = StringField('Información de contacto', render_kw={"class": "form-control"})   
    paginacion = IntegerField('Cantidad de elementos por página', render_kw={"class": "form-control"})
    sitio_habilitado = BooleanField('Habilitar sitio')
    submit = SubmitField('Guardar cambios', render_kw={"class": "btn btn-lg btn-primary btn-block"})
    
class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email("Ingrese un email válido")], render_kw={"class": "form-control"})
    username = StringField('Nombre de usuario', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Contraseña', validators=[DataRequired()], render_kw={"class": "form-control"})
    first_name = StringField('Nombre', validators=[DataRequired()], render_kw={"class": "form-control"})
    last_name = StringField('Apellido', validators=[DataRequired()], render_kw={"class": "form-control"})
    rol = SelectField('Rol', render_kw={"class": "form-control"})
    submit = SubmitField('Registrar usuario', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class SignUpEstudianteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()], render_kw={"class": "form-control"})
    apellido = StringField('Apellido', validators=[DataRequired()], render_kw={"class": "form-control"})
    fecha_nac = DateField('Fecha de nacimiento', validators=[DataRequired()], render_kw={"class": "form-control"})
    localidad = SelectField('Localidad', validators=[DataRequired()], render_kw={"class": "form-control"})
    nivel = SelectField('Nivel', validators=[DataRequired()], render_kw={"class": "form-control"})
    domicilio = StringField('Domicilio', validators=[DataRequired()], render_kw={"class": "form-control"})
    genero = SelectField('Género', validators=[DataRequired()], render_kw={"class": "form-control"})
    escuela = SelectField('Escuela', validators=[DataRequired()], render_kw={"class": "form-control"})
    tipo_doc = SelectField('Tipo de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    numero = StringField('Número de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    tel = StringField('Teléfono', validators=[DataRequired()], render_kw={"class": "form-control"})
    barrio = SelectField('Barrio', validators=[DataRequired()], render_kw={"class": "form-control"})
    tipo_responsable = SelectField('Tipo de responsable', validators=[DataRequired()], render_kw={"class": "form-control"})
    responsable = SelectField('Responsable', validators=[DataRequired()], render_kw={"class": "form-control"})

    submit = SubmitField('Registrar estudiante', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class EditarEstudianteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()], render_kw={"class": "form-control"})
    apellido = StringField('Apellido', validators=[DataRequired()], render_kw={"class": "form-control"})
    fecha_nac = DateField('Fecha de nacimiento', validators=[DataRequired()], render_kw={"class": "form-control"})
    localidad = SelectField('Localidad', validators=[DataRequired()], render_kw={"class": "form-control"})
    nivel = SelectField('Nivel', validators=[DataRequired()], render_kw={"class": "form-control"})
    domicilio = StringField('Domicilio', validators=[DataRequired()], render_kw={"class": "form-control"})
    genero = SelectField('Género', validators=[DataRequired()], render_kw={"class": "form-control"})
    escuela = SelectField('Escuela', validators=[DataRequired()], render_kw={"class": "form-control"})
    tipo_doc = SelectField('Tipo de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    numero = StringField('Número de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    tel = StringField('Teléfono', validators=[DataRequired()], render_kw={"class": "form-control"})
    barrio = IntegerField('Barrio', validators=[DataRequired()], render_kw={"class": "form-control"})
    tipo_responsable = SelectField('Tipo de responsable', validators=[DataRequired()], render_kw={"class": "form-control"})
    responsable = SelectField('Responsable', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Editar estudiante', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})

class EditarDocenteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()], render_kw={"class": "form-control"})
    apellido = StringField('Apellido', validators=[DataRequired()], render_kw={"class": "form-control"})
    fecha_nac = DateField('Fecha de nacimiento', validators=[DataRequired()], render_kw={"class": "form-control"})
    localidad = SelectField('Localidad', validators=[DataRequired()], render_kw={"class": "form-control"})
    domicilio = StringField('Domicilio', validators=[DataRequired()], render_kw={"class": "form-control"})
    genero = SelectField('Género', validators=[DataRequired()], render_kw={"class": "form-control"})
    tipo_doc = SelectField('Tipo de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    numero = StringField('Número de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    tel = StringField('Teléfono', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Editar', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class SignUpDocenteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()], render_kw={"class": "form-control"})
    apellido = StringField('Apellido', validators=[DataRequired()], render_kw={"class": "form-control"})
    fecha_nac = DateField('Fecha de nacimiento', validators=[DataRequired()], render_kw={"class": "form-control"})
    localidad = SelectField('Localidad', validators=[DataRequired()], render_kw={"class": "form-control"})
    domicilio = StringField('Domicilio', validators=[DataRequired()], render_kw={"class": "form-control"})
    genero = SelectField('Género', render_kw={"class": "form-control"})
    tipo_doc = SelectField('Tipo de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    numero = StringField('Número de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    tel = StringField('Teléfono', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Registrar', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})

class SignUpCicloLectivoForm(FlaskForm):
    fecha_ini = DateField('Fecha de inicio', validators=[DataRequired()], render_kw={"class": "form-control"})
    fecha_fin = DateField('Fecha de finalizacion', validators=[DataRequired()], render_kw={"class": "form-control"})
    semestre = SelectField('Semestre', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Registrar ciclo lectivo', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class EditarForm(FlaskForm):
    email = EmailField('Email', validators=[Email("Ingrese un email válido")], render_kw={"class": "form-control"})
    username = StringField('Nombre de usuario', render_kw={"class": "form-control"})
    first_name = StringField('Nombre', render_kw={"class": "form-control"})
    last_name = StringField('Apellido', render_kw={"class": "form-control"})
    agregar_rol = SelectField('Agregar rol', render_kw={"class": "form-control"})
    quitar_rol = SelectField('Quitar rol', render_kw={"class": "form-control"})
    submit = SubmitField('Editar usuario', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    

class EditarCicloLectivoForm(FlaskForm):
    fecha_ini = DateField('Fecha de inicio', validators=[DataRequired()], render_kw={"class": "form-control"})
    fecha_fin = DateField('Fecha de finalizacion', validators=[DataRequired()], render_kw={"class": "form-control"})
    semestre = SelectField('Semestre', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Editar ciclo lectivo', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class BusquedaUsuarioForm(FlaskForm):
    rol = SelectField('Buscar por rol', render_kw={"class": "form-control"})
    termino = StringField('Buscar por nombre de usuario', render_kw={"class": "form-control"})
    activos = BooleanField('Usuarios activos')
    inactivos = BooleanField('Usuarios inactivos')
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary pb-20", "style": "margin: 20px"})
    
class BusquedaEstudianteForm(FlaskForm):
    ciclo = StringField()
    taller = StringField()
    termino = StringField('Buscar por nombre o apellido', render_kw={"class": "form-control"})
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary", "style": "margin-top: 20px"})

class BusquedaTallerForm(FlaskForm):
    ciclo = StringField()
    termino = StringField('Buscar por nombre o nombre corto', render_kw={"class": "form-control"})
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary", "style": "margin-top: 20px"})
    
class BusquedaDocenteForm(FlaskForm):
    ciclo = StringField()
    taller = StringField()
    termino = StringField('Buscar por nombre o apellido', render_kw={"class": "form-control"})
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary", "style": "margin-top: 20px"})

class BusquedaCicloLectivoForm(FlaskForm):
    termino = StringField('Buscar por año', render_kw={"class": "form-control"})
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary", "style": "margin-top: 20px"})


class InstrumentoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()], render_kw={"class": "form-control"})
    numero_inventario = StringField('Número de inventario', validators=[DataRequired()], render_kw={"class": "form-control"})
    tipo_instrumento = SelectField('Tipo de instrumento', validators=[DataRequired()], render_kw={"class": "form-control"})
    foto = FileField('Foto', validators=[DataRequired()])
    submit = SubmitField('Registrar', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})

class BusquedaInstrumentoForm(FlaskForm):
    termino = StringField('Buscar número de inventario', render_kw={"class": "form-control"})
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary", "style": "margin-top: 20px"})
    
class BusquedaAsistenciaForm(FlaskForm):
    termino = StringField('Buscar por nombre de taller', render_kw={"class": "form-control"})
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary", "style": "margin-top: 20px"})
    
class PasarAsistenciaForm(FlaskForm):
    estado = SelectField('Presente/Ausente',render_kw={"class": "form-control"})
    id = StringField('id', render_kw={"style": "display: none"})
    submit = SubmitField('Pasar', render_kw={"class": "btn btn-primary"})
    
class AsignarHorarioTallerForm(FlaskForm):
    profesor =SelectField('Profesor', validators=[DataRequired()], render_kw={"class": "form-control"})
    nucleo =SelectField('Nucleo', validators=[DataRequired()], render_kw={"class": "form-control"})
    hora_inicio =TimeField('Hora inicio', validators=[DataRequired()], render_kw={"class": "form-control"})
    hora_fin =TimeField('Hora fin', validators=[DataRequired()], render_kw={"class": "form-control"})
    dia =SelectField('Día', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Asignar', render_kw={"class": "btn btn-primary", "style": "margin-top: 20px"})