from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.usuarios_service import UsuarioService 
import json 

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        email = request.form['email']
        rol = request.form['rol']

        usuarios = UsuarioService.obtener_usuarios()  
        nuevo_usuario = {
            "id": str(len(usuarios) + 1),  
            "usuario": usuario,
            "contrasena": contrasena,
            "email": email,
            "rol": rol
        }

        try:
            if UsuarioService.agregar_usuario(nuevo_usuario):
                flash("Usuario agregado exitosamente.", "success")
                return redirect(url_for('usuario.ver_usuarios')) 
            else:
                flash("Error al agregar el usuario.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}", "danger")

    return render_template('usuario/agregar_usuario.html')




@usuario_bp.route('/editar_usuario/<id_usuario>', methods=['GET', 'POST'])
def editar_usuario(id_usuario):
    usuario_a_editar = UsuarioService.obtener_usuario_por_id(id_usuario) 

    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        email = request.form['email']
        rol = request.form['rol']

        usuario_actualizado = {
            "id": id_usuario,
            "usuario": usuario,
            "contrasena": contrasena,
            "email": email,
            "rol": rol
        }

        try:
            if UsuarioService.actualizar_usuario(usuario_actualizado): 
                flash("Usuario actualizado exitosamente.", "success")
                return redirect(url_for('usuario.ver_usuarios')) 
            else:
                flash("Error al actualizar el usuario.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}", "danger")

    return render_template('usuario/editar_usuario.html', usuario=usuario_a_editar)


@usuario_bp.route('/eliminar_usuario/<id_usuario>', methods=['POST'])
def eliminar_usuario(id_usuario):
    try:
        if UsuarioService.eliminar_usuario(id_usuario):
            flash("Usuario eliminado exitosamente.", "success")
        else:
            flash("Error al eliminar el usuario.", "danger")
    except Exception as e:
        flash(f"Ocurrió un error: {str(e)}", "danger")

    return redirect(url_for('usuario.ver_usuarios'))


@usuario_bp.route('/ver_usuarios', methods=['GET'])
def ver_usuarios():
    usuarios = UsuarioService.obtener_usuarios()  
    return render_template('usuario/ver_usuarios.html', usuarios=usuarios)
