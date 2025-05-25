from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
from urllib.parse import urlparse

app = Flask(__name__)

# ✅ Conexión con base de datos en Railway
def get_db_connection():
    db_url = os.getenv("MYSQL_URL")
    result = urlparse(db_url)

    return mysql.connector.connect(
        host=result.hostname,
        user=result.username,
        password=result.password,
        database=result.path.lstrip('/'),
        port=result.port
    )

@app.route("/")
def index():
    return render_template("index.html")

# 🔍 Obtener todos los productos
@app.route("/productos", methods=["GET"])
def obtener_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return jsonify(productos)

# ➕ Agregar un nuevo producto
@app.route("/productos", methods=["POST"])
def agregar_producto():
    data = request.get_json()
    nombre = data.get("nombre")
    precio = data.get("precio")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Producto agregado correctamente"}), 201

# ❌ Eliminar un producto por ID
@app.route("/productos/<int:producto_id>", methods=["DELETE"])
def eliminar_producto(producto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Producto eliminado correctamente"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

