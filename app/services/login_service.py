from config import JSONBIN_URL_USUARIOS, HEADERS
import requests
from app.services.usuarios_service import UsuarioService 
import json

class LoginService:
    
    @staticmethod
    def autenticar_usuario(usuario_ingresado, contrasena_ingresada):
        usuarios = UsuarioService.obtener_usuarios()
        
        for usuario in usuarios:
            if usuario['usuario'] == usuario_ingresado and usuario['contrasena'] == contrasena_ingresada:
                return usuario 
        return None  