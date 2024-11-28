from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.login_service import LoginService  

autenticacion_bp = Blueprint('autenticacion', __name__)

@autenticacion_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_ingresado = request.form['usuarioIngresado']
        contrasena_ingresada = request.form['contrasenaIngresada']

        usuario_encontrado = LoginService.autenticar_usuario(usuario_ingresado, contrasena_ingresada)
        if usuario_encontrado:
            session['rol'] = usuario_encontrado['rol']
            session['usuario'] = usuario_encontrado

            return redirect(url_for('inicio.inicio')) 
        else:
            flash(f'Usuario "{usuario_ingresado}" o contraseña "{contrasena_ingresada}" incorrectos. Intenta nuevamente.')

    return render_template('autenticacion/login.html')

@autenticacion_bp.route('/registro')
def registro():
    return render_template('autenticacion/registro.html') 

@autenticacion_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('rol', None)
    flash('Has cerrado sesión exitosamente.')
    return redirect(url_for('inicio.inicio'))


