from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.services.wishlist_service import get_all_items, add_item, delete_item

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist', methods=['GET'])
def get_wishlist():
    try:
        usuario = session['usuario']
        items = get_all_items(usuario['id'])
        return render_template('wishlist/ver_wishlist.html', wishlist=items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wishlist_bp.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.json
    producto_id = data.get('producto_id')

    if not producto_id:
        return jsonify({"error": "El campo 'producto_id' es obligatorio"}), 400

    try:
        usuario = session['usuario']
        result = add_item(usuario['id'], producto_id)
        if "error" in result:
            return jsonify(result), 400
        return jsonify({"message": "Producto agregado exitosamente a la wishlist.", "id": result["id"]}), 201
    except KeyError:
        return jsonify({"error": "Usuario no autenticado o sesión inválida"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wishlist_bp.route('/wishlist/<int:item_id>', methods=['POST'])
def delete_from_wishlist(item_id):
    try:
        if 1 == delete_item(item_id):
            flash("Wishlist item eliminado exitosamente.", "success")
        else:
            flash("Error al eliminar el item de wishlist.", "danger")
    except Exception as e:
        flash(f"Ocurrió un error: {str(e)}", "danger")

    return redirect(url_for('wishlist.get_wishlist'))
