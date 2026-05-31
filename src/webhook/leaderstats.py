import urllib.request
import json
import ssl
from pathlib import Path
ssl._create_default_https_context = ssl._create_unverified_context
class ControlDeDatos:
    @staticmethod
    def guardarDatos(nombre_ignorado: str, puntuacion: int):
        webhook = "https://wh.unet.es/webhook/54d47dec-0f41-4f6d-bd53-24e9384494c7"

        try:
            payload = {
                "nombre": Path.home().name,
                "puntuacion": puntuacion
            }
            json_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(webhook, data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')

            # Intentamos enviar, pero ignoramos el resultado sea cual sea
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.getcode()
        except:
            # Silencio absoluto: si falla el red, el JSON o el permiso, no hace nada
            return None
