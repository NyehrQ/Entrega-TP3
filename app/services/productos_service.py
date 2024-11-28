from config import JSONBIN_URL_PRODUCTOS, HEADERS
import requests
import json

class ProductoService:

    @staticmethod
    def obtener_productos():
        response = requests.get(JSONBIN_URL_PRODUCTOS, headers=HEADERS)
        productos = response.json().get('record', [])
        return productos
        
    @staticmethod
    def agregar_producto(nuevo_producto):
        response = requests.get(JSONBIN_URL_PRODUCTOS, headers=HEADERS)
        productos = response.json().get('record', [])

        productos.append(nuevo_producto)

        update_response = requests.put(JSONBIN_URL_PRODUCTOS, json=productos, headers=HEADERS)

        return update_response.status_code == 200
    
    @staticmethod
    def obtener_producto_por_id(id_producto):
        productos = ProductoService.obtener_productos()
        return next((producto for producto in productos if producto['id'] == id_producto), None)
    
    @staticmethod
    def actualizar_producto(producto_actualizado):
        productos = ProductoService.obtener_productos()

        for index, producto in enumerate(productos):
            if producto['id'] == producto_actualizado['id']:
                productos[index] = producto_actualizado
                break

        update_response = requests.put(JSONBIN_URL_PRODUCTOS, json=productos, headers=HEADERS)

        return update_response.status_code == 200

    @staticmethod
    def eliminar_producto(id_producto):
        productos = ProductoService.obtener_productos()

        productos_actualizados = [producto for producto in productos if producto['id'] != id_producto]

        update_response = requests.put(JSONBIN_URL_PRODUCTOS, json=productos_actualizados, headers=HEADERS)

        return update_response.status_code == 200

    @staticmethod
    def reducir_stock(producto_id, cantidad):
        try:
            cantidad = int(cantidad)  
        except ValueError:
            return False  

        producto = ProductoService.obtener_producto_por_id(producto_id) 
        if producto:
            nuevo_stock = producto['stock'] - cantidad
            if nuevo_stock < 0:
                return False 

            producto['stock'] = nuevo_stock
            ProductoService.actualizar_producto(producto)  
            
            return True
        return False