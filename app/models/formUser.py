from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo,Email
import re


class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(max=100, message='El nombre no puede exceder los 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='El correo electrónico es obligatorio'),
        Length(max=120, message='El correo electrónico no puede exceder los 120 caracteres'),
        Email(message='El correo electrónico no es válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Debe confirmar la contraseña'),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    current_password = PasswordField('Contraseña Actual', validators=[
        DataRequired(message='La contraseña actual es obligatoria')
    ])
    submit = SubmitField('Guardar Cambios')

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email.data):
            raise ValidationError('El correo electrónico no es válido')
        
class UserForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='El correo electrónico es obligatorio'),
        Length(max=120, message='El correo electrónico no puede exceder los 120 caracteres'),
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
    ])

    def validate_correo(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email.data):
            raise ValidationError('El correo electrónico no es válido')