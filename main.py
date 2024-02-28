from flask import Flask, render_template, request, Response
import forms
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfigMain
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

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()