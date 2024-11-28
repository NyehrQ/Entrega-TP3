from config import JSONBIN_URL_USUARIOS, HEADERS
import requests
import json

class UsuarioService:
    
    @staticmethod
    def obtener_usuarios():
        response = requests.get(JSONBIN_URL_USUARIOS, headers=HEADERS)
        usuarios = response.json().get('record', [])
        return usuarios

    @staticmethod
    def agregar_usuario(nuevo_usuario):
        response = requests.get(JSONBIN_URL_USUARIOS, headers=HEADERS)
        usuarios = response.json().get('record', [])
        usuarios.append(nuevo_usuario)

        update_response = requests.put(JSONBIN_URL_USUARIOS, json=usuarios, headers=HEADERS)


        return update_response.status_code == 200
    
    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        usuarios = UsuarioService.obtener_usuarios()
        return next((usuario for usuario in usuarios if usuario['id'] == id_usuario), None)
    
    @staticmethod
    def actualizar_usuario(usuario_actualizado):
        usuarios = UsuarioService.obtener_usuarios()

        for index, usuario in enumerate(usuarios):
            if usuario['id'] == usuario_actualizado['id']:
                usuarios[index] = usuario_actualizado
                break

        update_response = requests.put(JSONBIN_URL_USUARIOS, json=usuarios, headers=HEADERS)

        return update_response.status_code == 200

    @staticmethod
    def eliminar_usuario(id_usuario):
        usuarios = UsuarioService.obtener_usuarios()

        usuarios_actualizados = [usuario for usuario in usuarios if usuario['id'] != id_usuario]
        update_response = requests.put(JSONBIN_URL_USUARIOS, json=usuarios_actualizados, headers=HEADERS)

        return update_response.status_code == 200
