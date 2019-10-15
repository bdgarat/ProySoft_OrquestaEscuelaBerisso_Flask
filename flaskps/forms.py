from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Contraseña', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Iniciar sesión', render_kw={"class": "btn btn-lg btn-primary btn-block"})