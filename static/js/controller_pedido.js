
let pizzas = [];

document.addEventListener('DOMContentLoaded', function () {

    if (document.getElementById('pizzas').value != '') {
        pizzas = JSON.parse(document.getElementById('pizzas').value);
    }else{
        pizzas = [];
        document.getElementById('fechaPedido').value = new Date().toISOString().split('T')[0];
    }

    loadPizzas();
});

document.getElementById('registro').addEventListener('submit', function(e) {
    e.preventDefault(); // Evita el envío del formulario
    
    Swal.fire({
        title: '¿Estás seguro de registrar el pedido?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Registrar'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                'Registrado',
                'El pedido ha sido registrado',
                'success'
            )
            // Si el usuario confirma, enviar el formulario
            document.getElementById('registro').submit();
            
        }
    });
});

function addPizza() {
    const tamanio = document.querySelector('input[name="tamanioPizza"]:checked').value;
    console.log(tamanio);
    
    let pina = document.getElementById('pina').checked;
    let jamon = document.getElementById('jamon').checked;
    let champin = document.getElementById('champin').checked;
    let salchicha = document.getElementById('salchicha').checked;
    let numPizzas = document.getElementById('numPizzas').value;
    subtotal = 0;

    ingredientes = [];

    if (tamanio == 'Chica') {
        subtotal += 40;
    } else if (tamanio == 'Mediana') {
        subtotal += 80;
    } else if (tamanio == 'Grande') {
        subtotal += 120;
    }

    if (pina) {
        ingredientes.push('Pina');
        subtotal += 10;
    }

    if (jamon) {
        ingredientes.push('Jamon');
        subtotal += 10;
    }

    if (champin) {
        ingredientes.push('Champin');
        subtotal += 10;
    }

    if (salchicha) {
        ingredientes.push('Salchicha');
        subtotal += 10;
    }

    subtotal = subtotal * numPizzas;

    pizza = {
        tamanio: tamanio,
        ingredientes: ingredientes,
        numPizzas: numPizzas,
        subtotal: subtotal
    }

    pizzas.push(pizza);
    alert("Pizza agregada");
    calcularTotal();
    document.getElementById('pizzas').value = JSON.stringify(pizzas);
    loadPizzas();
}

function loadPizzas() {
    const tabla = document.getElementById('tblPizzas');
    tabla.innerHTML = '';

    pizzas.forEach(pizza => {
        const row = tabla.insertRow();

        row.insertCell(0).textContent = pizza.tamanio;
        row.insertCell(1).textContent = pizza.ingredientes;
        row.insertCell(2).textContent = pizza.numPizzas;
        row.insertCell(3).textContent = pizza.subtotal;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Eliminar';
        deleteButton.class = 'btn btn-danger';
        deleteButton.addEventListener('click', () => {
            eliminarPizza(pizza);
            calcularTotal();
            document.getElementById('pizzas').value = JSON.stringify(pizzas);
        });
        row.insertCell(4).appendChild(deleteButton);
    });
}

function eliminarPizza(pizza) {
    const index = pizzas.indexOf(pizza);
    if (index !== -1) {
        pizzas.splice(index, 1);
        loadPizzas();
    }
}

function calcularTotal(){
    let total = 0;
    pizzas.forEach(pizza => {
        total += pizza.subtotal;
    })

    document.getElementById('total').value = total;
}