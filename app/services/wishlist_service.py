import mysql.connector
from config import db_config
from app.services.productos_service import ProductoService

def get_all_items(usuario_id):
    conn = None
    cursor = None
    try:
        productos = ProductoService.obtener_productos()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM wishlist WHERE usuario_id = %s", (usuario_id,))
        wishlist = cursor.fetchall()

        for item in wishlist:
            producto = next((p for p in productos if p["id"] == str(item["producto_id"])), None)
            item["nombre_producto"] = producto["nombre"] if producto else "Producto desconocido"

        return wishlist
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_item(usuario_id, producto_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM wishlist WHERE usuario_id = %s AND producto_id = %s",
            (usuario_id, producto_id)
        )
        if cursor.fetchone()[0] > 0:
            return {"error": "El producto ya está en la wishlist"}

        cursor.execute(
            "INSERT INTO wishlist (usuario_id, producto_id) VALUES (%s, %s)",
            (usuario_id, producto_id)
        )
        conn.commit()
        return {"success": True, "id": cursor.lastrowid}
    except mysql.connector.Error as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_item(item_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wishlist WHERE id = %s", (item_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
