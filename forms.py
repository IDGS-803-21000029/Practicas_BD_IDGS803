from wtforms import Form
from wtforms import StringField, EmailField, IntegerField, DecimalField
from wtforms import validators

class EmployeeForm(Form):
    id = IntegerField('id')
    nombre = StringField('Nombre', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=4, max=25)])
    correo = EmailField('Email', [validators.DataRequired(message='Ingresa un Correo Valido')])
    telefono = IntegerField('Telefono', [validators.DataRequired(message='El campo es requerido'), validators.NumberRange(min=2, max=10000000000)])
    direccion = StringField('Direccion', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=4, max=200)])
    sueldo = DecimalField('Sueldo', [validators.DataRequired(message='El campo es requerido'), validators.NumberRange(min=0, max=1000000)])