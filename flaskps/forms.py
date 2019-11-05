from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField, DateField


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
    localidad = IntegerField('Localidad', validators=[DataRequired()], render_kw={"class": "form-control"})
    nivel = IntegerField('Nivel', validators=[DataRequired()], render_kw={"class": "form-control"})
    domicilio = StringField('Domicilio', validators=[DataRequired()], render_kw={"class": "form-control"})
    genero = IntegerField('Género', validators=[DataRequired()], render_kw={"class": "form-control"})
    escuela = IntegerField('Escuela', validators=[DataRequired()], render_kw={"class": "form-control"})
    tipo_doc = IntegerField('Tipo de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    numero = StringField('Número de documento', validators=[DataRequired()], render_kw={"class": "form-control"})
    tel = StringField('Teléfono', validators=[DataRequired()], render_kw={"class": "form-control"})
    barrio = IntegerField('Barrio', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Registrar estudiante', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class EditarForm(FlaskForm):
    email = EmailField('Email', validators=[Email("Ingrese un email válido")], render_kw={"class": "form-control"})
    username = StringField('Nombre de usuario', render_kw={"class": "form-control"})
    first_name = StringField('Nombre', render_kw={"class": "form-control"})
    last_name = StringField('Apellido', render_kw={"class": "form-control"})
    agregar_rol = SelectField('Agregar rol', render_kw={"class": "form-control"})
    quitar_rol = SelectField('Quitar rol', render_kw={"class": "form-control"})
    submit = SubmitField('Editar usuario', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class BusquedaUsuarioForm(FlaskForm):
    rol = SelectField('Buscar por rol', render_kw={"class": "form-control"})
    termino = StringField('Buscar por nombre de usuario', render_kw={"class": "form-control"})
    activos = BooleanField('Usuarios activos')
    inactivos = BooleanField('Usuarios inactivos')
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary pb-20"})
    
class BusquedaEstudianteForm(FlaskForm):
    termino = StringField('Buscar por nombre o apellido', render_kw={"class": "form-control"})
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary"})
