from flask import Blueprint, render_template
from app.services.usuarios_service import UsuarioService 

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/index')
def dashboard():
    return render_template('dashboard/index.html')

