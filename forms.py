from wtforms import Form
from wtforms import StringField, EmailField, IntegerField, DecimalField, DateField, RadioField, BooleanField, SelectField
from wtforms import validators


class EmployeeForm(Form):
    id = IntegerField('id')
    nombre = StringField('Nombre', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=4, max=25)])
    correo = EmailField('Email', [validators.DataRequired(message='Ingresa un Correo Valido')])
    telefono = IntegerField('Telefono', [validators.DataRequired(message='El campo es requerido'), validators.NumberRange(min=2, max=10000000000)])
    direccion = StringField('Direccion', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=4, max=200)])
    sueldo = DecimalField('Sueldo', [validators.DataRequired(message='El campo es requerido'), validators.NumberRange(min=0, max=1000000)])


class PedidoForm(Form):
    id = IntegerField('id')
    nombreCliente = StringField('Nombre', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=4, max=250)])
    direccionEnvio = StringField('Direccion', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=4, max=250)])
    telefono = StringField('Telefono', [validators.DataRequired(message='El campo es requerido'), validators.NumberRange(min=2, max=20)])
    fechaPedido = DateField('FechaPedido', [validators.DataRequired(message='El campo es requerido')])
    tamanioPizza = RadioField('Tamanio', choices=[('Chica', 'Chica $40'), ('Mediana', 'Mediana $80'), ('Grande', 'Grande $120')])
    #Ingredientes
    jamon = BooleanField('Jamon $10')
    pina = BooleanField('Piña $10')
    champin = BooleanField('Champiñones $10')
    salchicha = BooleanField('Salchicha $10')
    numPizzas = IntegerField('Pizzas', [validators.DataRequired(message='El campo es requerido'), validators.NumberRange(min=1, max=10)])
    total = DecimalField('Total', [validators.DataRequired(message='El campo es requerido'), validators.NumberRange(min=0, max=1000000)])
    pizzas = StringField('Pizzas Array', [validators.DataRequired(message='El campo es requerido')])

class FiltroForm(Form):
    dia = SelectField('Dia', choices=[('', 'Seleccione un Dia'), ('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')])
    mes = SelectField('Mes', choices=[('00', 'Seleccione un Mes'), ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'), ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')])
