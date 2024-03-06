from flask import Flask, render_template, request, Response
from forms import EmployeeForm, PedidoForm, FiltroForm
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfigMain
from flask import redirect
from models import db
from models import Empleados, detallePedido, encabPedido
import json
from datetime import datetime
from sqlalchemy import extract

app = Flask(__name__)
app.config.from_object(DevelopmentConfigMain)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_find(e):
    return render_template('404.html'),404

@app.route("/empleados", methods=["GET", "POST"])
def index():
    emp_form = EmployeeForm(request.form)
    if request.method == 'POST':
        emp = Empleados(nombre = emp_form.nombre.data,
                        correo = emp_form.correo.data,
                        telefono = emp_form.telefono.data,
                        direccion = emp_form.direccion.data,
                        sueldo = emp_form.sueldo.data)

        db.session.add(emp)
        db.session.commit()

    return render_template("empleados.html", form=emp_form)

@app.route("/tblempleados", methods=["GET", "POST"])
def ABC_Completo():
    empleados = Empleados.query.all()
    return render_template("tblempleados.html", empleados=empleados)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    emp_form = EmployeeForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        emp1 = db.session.query(Empleados).filter_by(id=id).first()
        emp_form.id.data = request.args.get('id')
        emp_form.nombre.data = emp1.nombre
        emp_form.correo.data = emp1.correo
        emp_form.telefono.data = emp1.telefono
        emp_form.direccion.data = emp1.direccion
        emp_form.sueldo.data = emp1.sueldo
    elif request.method == 'POST':
        id = emp_form.id.data
        emp = Empleados.query.get(id)
        db.session.delete(emp)
        db.session.commit()
        return redirect('/tblempleados')
    
    return render_template("eliminar.html", form=emp_form)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    emp_form = EmployeeForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        emp1 = db.session.query(Empleados).filter_by(id=id).first()
        emp_form.id.data = request.args.get('id')
        emp_form.nombre.data = emp1.nombre
        emp_form.correo.data = emp1.correo
        emp_form.telefono.data = emp1.telefono
        emp_form.direccion.data = emp1.direccion
        emp_form.sueldo.data = emp1.sueldo
    elif request.method == 'POST':
        id = emp_form.id.data
        emp = Empleados.query.get(id)
        emp.nombre = emp_form.nombre.data
        emp.correo = emp_form.correo.data
        emp.telefono = emp_form.telefono.data
        emp.direccion = emp_form.direccion.data
        emp.sueldo = emp_form.sueldo.data
        db.session.add(emp)
        db.session.commit()
        return redirect('/tblempleados')
    
    return render_template("modificar.html", form=emp_form)


from datetime import datetime

@app.route("/pizzeria")
def pizzeria():
    filtro_form = FiltroForm(request.form)
    fecha_filtro = request.args.get('dia')
    mes_filtro : str = request.args.get('mes')
    print(fecha_filtro, mes_filtro)
    print(type(fecha_filtro), type(mes_filtro))

    if fecha_filtro:
        fecha_obj = datetime.strptime(fecha_filtro, '%Y-%m-%d')
        pedidos = encabPedido.query.filter(encabPedido.fechaCompra == fecha_obj).all()
    elif mes_filtro and mes_filtro != '00':
        mes_obj = datetime.strptime(mes_filtro, '%m')
        pedidos = encabPedido.query.filter(extract('month', encabPedido.fechaCompra) == mes_obj.month).all()
    else:
        pedidos = encabPedido.query.all()

    return render_template("pizzeria.html", pedidos=pedidos, form=filtro_form)


@app.route("/pedidos", methods=["GET", "POST"])
def pedidos():
    ped_form = PedidoForm(request.form)
    if request.method == 'POST':
        pizzas = ped_form.pizzas.data
        print(pizzas)
        nombre = ped_form.nombreCliente.data
        direccion = ped_form.direccionEnvio.data
        telefono = ped_form.telefono.data
        fecha = ped_form.fechaPedido.data
        print(nombre, direccion, telefono, fecha)

        pizzas_json = json.loads(pizzas)

        encabezado = encabPedido(
            nombreCliente = ped_form.nombreCliente.data,
            direccionEnvio = ped_form.direccionEnvio.data,
            telefono = ped_form.telefono.data,
            totalCompra = ped_form.total.data
        )

        db.session.add(encabezado)
        db.session.commit()

        pedido = encabPedido.query.order_by(encabPedido.id_pedido.desc()).first()

        for piz in pizzas_json:
            pizza = detallePedido(
                tamanioPizza=piz['tamanio'],
                ingredientes="'" + "', '".join(piz['ingredientes']) + "'",
                numPizzas=piz['numPizzas'],
                subtotal=piz['subtotal'],
                id_pedido=pedido.id_pedido
            )

            db.session.add(pizza)
            db.session.commit()

        return redirect('/pizzeria')
    
    elif request.method == 'GET':
        if request.args.get('id'):
            id = request.args.get('id')
            ped1 = db.session.query(encabPedido).filter_by(id_pedido=id).first() 
            ped_form.nombreCliente.data = ped1.nombreCliente
            ped_form.direccionEnvio.data = ped1.direccionEnvio
            ped_form.telefono.data = ped1.telefono
            ped_form.total.data = ped1.totalCompra
            ped_form.fechaPedido.data = ped1.fechaCompra
            ped_form.id.data = request.args.get('id')
            pizzasDet = db.session.query(detallePedido).filter_by(id_pedido=id).all()

            pizzas = []
            for piz in pizzasDet:
                pizzas.append({'tamanio': piz.tamanioPizza, 'ingredientes': piz.ingredientes.split("', '"), 'numPizzas': piz.numPizzas, 'subtotal': piz.subtotal})

            print(pizzas)
            ped_form.pizzas.data = json.dumps(pizzas)
        
    return render_template("pedido.html", form=ped_form)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()