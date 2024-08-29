from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class PropertyForm(FlaskForm):
    street = StringField('Calle', validators=[
        DataRequired(message='La dirección es obligatoria'),
        Length(max=255, message='La dirección no puede exceder los 255 caracteres')
    ])
    streetNumber = IntegerField('Altura', validators=[
        DataRequired(message='La altura es obligatoria'),
        NumberRange(min=0, message='La altura debe ser mayor o igual a 0')
    ])
    description = StringField('Descripción', validators=[
        DataRequired(message='La descripción es obligatoria'),
        Length(max=500, message='La descripción no puede exceder los 500 caracteres')
    ])
    city = StringField('Ciudad', validators=[
        DataRequired(message='La ciudad es obligatoria'),
        Length(max=255, message='La ciudad no puede exceder los 255 caracteres')
    ])
    price = IntegerField('Precio', validators=[
        DataRequired(message='El precio es obligatorio'),
        NumberRange(min=0, message='El precio debe ser mayor o igual a 0')
    ])
    rooms = IntegerField('Habitaciones', validators=[
        DataRequired(message='La cantidad de habitaciones es obligatoria'),
        NumberRange(min=0, message='La cantidad de habitaciones debe ser mayor a 0')
    ])
    squareMeters = IntegerField('Metros Cuadrados', validators=[
        DataRequired(message='Los metros cuadrados son obligatorios'),
        NumberRange(min=1, message='Los metros cuadrados deben ser mayores a 0')
    ])
    image = FileField('Imagenes', validators=[], render_kw={"multiple": True})