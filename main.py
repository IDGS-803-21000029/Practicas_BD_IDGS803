from flask import Flask, render_template, request, Response
import forms
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfigMain
from flask import redirect
from models import db
from models import Empleados

app = Flask(__name__)
app.config.from_object(DevelopmentConfigMain)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_find(e):
    return render_template('404.html'),404

@app.route("/empleados", methods=["GET", "POST"])
def index():
    emp_form = forms.EmployeeForm(request.form)
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
    emp_form = forms.EmployeeForm(request.form)
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
    emp_form = forms.EmployeeForm(request.form)
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



if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()