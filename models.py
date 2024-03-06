from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Empleados(db.Model):
    __tablename__='empleados'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    correo=db.Column(db.String(50))
    telefono=db.Column(db.String(20))
    direccion=db.Column(db.String(200))
    sueldo=db.Column(db.Float(50))
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)


class encabPedido(db.Model):
    __tablename__ = 'encabPedido'
    id_pedido = db.Column(db.Integer, primary_key=True)
    nombreCliente = db.Column(db.String(250))
    direccionEnvio = db.Column(db.String(250))
    telefono = db.Column(db.String(20))
    fechaCompra = db.Column(db.Date, default=datetime.datetime.now().date())
    totalCompra = db.Column(db.Float)

class detallePedido(db.Model):
    __tablename__ = 'detallePedido'
    id_detalle = db.Column(db.Integer, primary_key=True)
    tamanioPizza = db.Column(db.String(20))
    ingredientes = db.Column(db.String(200))
    numPizzas = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    id_pedido = db.Column(db.Integer, db.ForeignKey('encabPedido.id_pedido'))
