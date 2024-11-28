from flask import Flask
from app.blueprints.autenticacion.rutas import autenticacion_bp
from app.blueprints.dashboard.rutas import dashboard_bp

def create_app():
    app = Flask(__name__)

    
    app.register_blueprint(autenticacion_bp)
    app.register_blueprint(dashboard_bp)

    return app
