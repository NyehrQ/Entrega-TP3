from flask import session, redirect, url_for, render_template, flash, Blueprint, request, jsonify
from app.services.productos_service import ProductoService
from app.services.ventas_service import VentasService
import uuid  # Para generar IDs únicos

inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route('/')
def index():
    productos = ProductoService.obtener_productos()  
    return render_template('inicio/inicio.html', productos=productos)

@inicio_bp.route('/inicio')
def inicio():
    productos = ProductoService.obtener_productos()  
    return render_template('inicio/inicio.html', productos=productos)

@inicio_bp.route('/ver_carrito')
def ver_carrito():
    return render_template('inicio/ver_carrito.html')

@inicio_bp.route('/realizar_pago')
def realizar_pago():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para realizar el pago.', 'warning')
        return redirect(url_for('autenticacion.login'))
    
    carrito = session.get('carrito', [])
    total = sum(item['precioTotal'] for item in carrito)

    return render_template('inicio/realizar_pago.html', carrito=carrito, total=total)

@inicio_bp.route('/procesar_pago', methods=['POST']) 
def procesar_pago():
    if 'usuario' not in session:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para realizar el pago.'}), 401

    nombre_tarjeta = request.form.get('nombreTarjeta')
    numero_tarjeta = request.form.get('numeroTarjeta')
    fecha_expiracion = request.form.get('fechaExpiracion')
    cvv = request.form.get('cvv')

    carrito = session.get('carrito', [])
    usuario_id = session.get('usuario', {}).get('id')  

    if not carrito:
        return jsonify({'success': False, 'message': 'El carrito está vacío.'}), 400

    venta_id = str(uuid.uuid4())

    nueva_venta = {
        "id": venta_id,
        "idUsuario": usuario_id
    }

    venta_agregada = VentasService.agregar_venta(nueva_venta)
    
    if not venta_agregada:
        return jsonify({'success': False, 'message': 'Hubo un error al registrar la venta.'}), 500

    for item in carrito:
        detalle_venta = {
            "id": str(uuid.uuid4()),  
            "idVenta": venta_id,
            "idProducto": item['id'],  
            "cantidad": item['cantidad'],
            "precio": item['precioUnitario'],
            "subtotal": item['precioTotal']
        }
        
        detalle_agregado = VentasService.agregar_detalle_venta(detalle_venta)
        
        if not detalle_agregado:
            return jsonify({'success': False, 'message': f'Error al registrar el detalle de venta para el producto {item["nombre"]}.'}), 500
        
        stock_reducido = ProductoService.reducir_stock(item['id'], item['cantidad'])
        if not stock_reducido:
            return jsonify({'success': False, 'message': f'Error al reducir el stock del producto {item["nombre"]}.'}), 500

    session.pop('carrito', None)
    return jsonify({'success': True})


@inicio_bp.route('/actualizar_carrito', methods=['POST'])
def actualizar_carrito():
    carrito = request.get_json()  
    if carrito:
        session['carrito'] = carrito  
        return jsonify({'success': True})
    return jsonify({'success': False})
