import requests
from bs4 import BeautifulSoup
import os


def get_html_body(target_url: str):
    soup = None
    
    # 1. Recuperamos la API KEY desde las variables de entorno (GitHub Secrets)

    if os.path.exits(".env"):
        from dotenv import load_dotenv
        load_dotenv()

    api_key = os.getenv("API_KEY")
    print(api_key)
    # 2. Configuración para ZenRows
    proxy_url = "https://api.zenrows.com/v1/"
    params = {
        'url': target_url,
        'apikey': api_key,
        'js_render': 'true',         # Renderiza JavaScript (necesario para PcComponentes)
        'premium_proxy': 'true'      # Usa IPs residenciales para evitar el 403
    }
    
    try:
        # 3. Hacemos la petición a través de ZenRows, no directo a la web
        print(f"Solicitando datos a ZenRows para: {target_url}")
        response = requests.get(proxy_url, params=params, timeout=60)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Error de la API: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"Error al conectar con el proxy: {e}")
        
    return soup