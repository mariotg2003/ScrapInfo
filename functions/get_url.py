import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def get_html_body(target_url: str):
    soup = None

    api_key = os.getenv("SCRAPE_TOKEN")

    if not api_key:
        print("No se encontró un token válido de Scrape.do")
        return None

    proxy_url = "https://api.scrape.do"
    params = {
        "token": api_key.strip(),
        "url": target_url,
        "render": "true",
        "wait": 5000,
        "premium_proxy": "true",
    }

    try:
        response = requests.get(proxy_url, params=params, timeout=60)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Error de la API Scrape.do: {response.status_code}")
            print(f"Respuesta: {response.text}")

    except Exception as e:
        print(f"Error al conectar con Scrape.do: {e}")

    return soup