from config import JSONBIN_URL_VENTA, JSONBIN_URL_VENTA_DETALLE, JSONBIN_URL_USUARIOS,JSONBIN_URL_PRODUCTOS, HEADERS  
import requests
import json
from datetime import datetime
from collections import defaultdict

class VentasService:
    
    @staticmethod
    def obtener_ventas():
        try:
            response = requests.get(JSONBIN_URL_VENTA, headers=HEADERS)
            ventas = response.json().get('record', [])
            return ventas
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener ventas: {e}")
            return []

    # Este metodo lo tenemos creado en usaurios_service, pero por miedo a tocarlo lo cree aca devuelta, por las dudas de pisarnos el codigo
    @staticmethod
    def obtener_usuarios():
        try:
            response = requests.get(JSONBIN_URL_USUARIOS, headers=HEADERS)  
            usuarios = response.json().get('record', [])
            return usuarios
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener usuarios: {e}")
            return []     

    @staticmethod
    def agregar_venta(nueva_venta):
        try:
            response = requests.get(JSONBIN_URL_VENTA, headers=HEADERS)
            ventas = response.json().get('record', [])

            # Agregar fecha actual
            nueva_venta['fecha'] = datetime.now().strftime("%d/%m/%Y")  
            ventas.append(nueva_venta)

            update_response = requests.put(JSONBIN_URL_VENTA, json=ventas, headers=HEADERS)

            return update_response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error al agregar venta: {e}")
            return False
           
    @staticmethod
    def obtener_ventas_detalle():
        try:
            response = requests.get(JSONBIN_URL_VENTA_DETALLE, headers=HEADERS)
            ventas_detalle = response.json().get('record', [])
            return ventas_detalle
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener ventas: {e}")
            return []  

    @staticmethod
    def obtener_venta_por_id(id_venta):
        try:
            ventas = VentasService.obtener_ventas()
            return next((venta for venta in ventas if venta['id'] == id_venta), None)
        except Exception as e:
            print(f"Error al obtener la venta por ID: {e}")
            return None
    
    @staticmethod
    def actualizar_venta(venta_actualizada):
        try:
            ventas = VentasService.obtener_ventas()

            for index, venta in enumerate(ventas):
                if venta['id'] == venta_actualizada['id']:
                    ventas[index] = venta_actualizada
                    break

            update_response = requests.put(JSONBIN_URL_VENTA, json=ventas, headers=HEADERS)
            return update_response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error al actualizar la venta: {e}")
            return False

    @staticmethod
    def eliminar_venta(id_venta):
        try:
            ventas = VentasService.obtener_ventas()
            ventas_actualizadas = [venta for venta in ventas if venta['id'] != id_venta]

            update_response = requests.put(JSONBIN_URL_VENTA, json=ventas_actualizadas, headers=HEADERS)
            return update_response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error al eliminar la venta: {e}")
            return False

    @staticmethod
    def agregar_detalle_venta(nuevo_detalle):
        try:
            response = requests.get(JSONBIN_URL_VENTA_DETALLE, headers=HEADERS)
            detalles_venta = response.json().get('record', [])

            detalles_venta.append(nuevo_detalle)

            update_response = requests.put(JSONBIN_URL_VENTA_DETALLE, json=detalles_venta, headers=HEADERS)
            return update_response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error al agregar detalle de venta: {e}")
            return False

    # @staticmethod
    # def obtener_detalles_venta_por_id_venta(id_venta):
    #     try:
    #         response = requests.get(JSONBIN_URL_VENTA_DETALLE, headers=HEADERS)
    #         detalles_venta = response.json().get('record', [])
    #         return [detalle for detalle in detalles_venta if detalle['idVenta'] == id_venta]
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error al obtener detalles de venta: {e}")
    #         return []

    @staticmethod
    def obtener_detalles_venta_por_id_venta(id_venta):
        try:
            response_detalle = requests.get(JSONBIN_URL_VENTA_DETALLE, headers=HEADERS)
            detalles_venta = response_detalle.json().get('record', [])
    
            response_productos = requests.get(JSONBIN_URL_PRODUCTOS, headers=HEADERS)
            productos = response_productos.json().get('record', [])

            productos_dict = {producto['id']: producto['nombre'] for producto in productos}
        
            return [
            {
                **detalle,
                'nombre_producto': productos_dict.get(detalle['idProducto'], 'Desconocido')
            }
            for detalle in detalles_venta if detalle['idVenta'] == id_venta
        ]
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener detalles de venta: {e}")
            return []


    @staticmethod
    def eliminar_detalles_venta_por_id_venta(id_venta):
        try:
            response = requests.get(JSONBIN_URL_VENTA_DETALLE, headers=HEADERS)
            detalles_venta = response.json().get('record', [])

            detalles_venta_actualizados = [detalle for detalle in detalles_venta if detalle['idVenta'] != id_venta]

            update_response = requests.put(JSONBIN_URL_VENTA_DETALLE, json=detalles_venta_actualizados, headers=HEADERS)
            return update_response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error al eliminar detalles de venta: {e}")
            return False
        
        
    @staticmethod
    def obtener_estadisticas():
        ventas = VentasService.obtener_ventas()

        total_ventas = len(ventas)

        ventas_por_mes = defaultdict(int)
        for venta in ventas:
            fecha = datetime.strptime(venta['fecha'], "%d/%m/%Y")
            mes = fecha.strftime("%Y-%m")  
            ventas_por_mes[mes] += 1

        meses = sorted(ventas_por_mes.keys())
        ventas_por_mes_values = [ventas_por_mes[mes] for mes in meses]

        promedio_ventas = total_ventas / len(ventas_por_mes) if ventas_por_mes else 0

        ventas_por_usuario = defaultdict(int)
        for venta in ventas:
            id_usuario = venta['idUsuario']
            ventas_por_usuario[id_usuario] += 1

        usuarios = list(ventas_por_usuario.keys())
        ventas_por_usuario_values = list(ventas_por_usuario.values())

        ultima_venta = max(ventas, key=lambda v: datetime.strptime(v['fecha'], "%d/%m/%Y"))['fecha'] if ventas else None

        return {
            'total_ventas': total_ventas,
            'promedio_ventas': promedio_ventas,
            'ultima_venta': ultima_venta,
            'meses': meses,
            'ventas_por_mes': ventas_por_mes_values,
            'usuarios': usuarios,
            'ventas_por_usuario': ventas_por_usuario_values
        }
        
    @staticmethod
    def obtener_venta_detalle_por_id(id_venta):
        try:
            ventas_detalle = VentasService.obtener_ventas_detalle()
            print(f"Buscando venta con ID: {id_venta}")
            return next((venta_detalle for venta_detalle in ventas_detalle if venta_detalle['idVenta'] == id_venta), None)
        except Exception as e:
            print(f"Error al obtener la venta por ID: {e}")
            return None    
