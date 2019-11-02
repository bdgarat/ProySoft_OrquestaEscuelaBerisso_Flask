from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField, DateField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Contraseña', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Iniciar sesión', render_kw={"class": "btn btn-lg btn-primary btn-block"})
    
class ConfigForm(FlaskForm):   
    titulo = StringField('Titulo del sitio', render_kw={"class": "form-control"})
    descripcion = StringField('Descripcion', render_kw={"class": "form-control"})   
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
    es_admin = BooleanField('Administrador', render_kw={"class": "col"})
    es_preceptor = BooleanField('Preceptor', render_kw={"class": "col"})
    es_docente = BooleanField('Docente', render_kw={"class": "col"})
    es_estudiante = BooleanField('Estudiante', render_kw={"class": "col"})
    submit = SubmitField('Registrar usuario', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class SignUpEstudianteForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email("Ingrese un email válido")], render_kw={"class": "form-control"})
    first_name = StringField('Nombre', validators=[DataRequired()], render_kw={"class": "form-control"})
    last_name = StringField('Apellido', validators=[DataRequired()], render_kw={"class": "form-control"})
    birth_date = DateField('Fecha de nacimiento', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Registrar usuario', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class EditarForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email("Ingrese un email válido")], render_kw={"class": "form-control"})
    username = StringField('Nombre de usuario', validators=[DataRequired()], render_kw={"class": "form-control"})
    first_name = StringField('Nombre', validators=[DataRequired()], render_kw={"class": "form-control"})
    last_name = StringField('Apellido', validators=[DataRequired()], render_kw={"class": "form-control"})
    es_admin = BooleanField('Administrador', render_kw={"class": "col"})
    es_preceptor = BooleanField('Preceptor', render_kw={"class": "col"})
    es_docente = BooleanField('Docente', render_kw={"class": "col"})
    submit = SubmitField('Editar usuario', render_kw={"class": "btn btn-lg btn-primary btn-block pb-20"})
    
class BusquedaForm(FlaskForm):
    termino = StringField('Buscar por nombre de usuario', render_kw={"class": "form-control"})
    submit = SubmitField('Buscar', render_kw={"class": "btn btn-primary pb-20"})
    activos = BooleanField('Usuarios activos')
    inactivos = BooleanField('Usuarios inactivos')
