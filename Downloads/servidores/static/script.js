async function cargarProductos() {
    let respuesta = await fetch('http://127.0.0.1:5000/productos');
    let productos = await respuesta.json();
    let tabla = document.getElementById('productos');
    tabla.innerHTML = '';
    let total = 0;
    productos.forEach(p => {
        tabla.innerHTML += `<tr>
            <td>${p.id}</td>
            <td>${p.nombre}</td>
            <td>${p.precio}</td>
            <td><button onclick="eliminarProducto(${p.id})">Eliminar</button></td>
        </tr>`;
        total += p.precio;
    });
    document.getElementById('total').textContent = total;
}

async function agregarProducto() {
    let nombre = document.getElementById('nombre').value;
    let precio = document.getElementById('precio').value;
    await fetch('http://127.0.0.1:5000/productos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, precio })
    });
    cargarProductos();
}

async function eliminarProducto(id) {
    await fetch(`http://127.0.0.1:5000/productos/${id}`, { method: 'DELETE' });
    cargarProductos();
}

cargarProductos();