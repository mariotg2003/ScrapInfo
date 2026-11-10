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
        "super": "true"
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


def get_html_body_with_fallback(target_url: str, fallback_url: str = ""):
    urls = [target_url]
    if fallback_url.strip():
        urls.append(fallback_url.strip())

    for index, url in enumerate(urls):
        tipo_url = "principal" if index == 0 else "de respaldo"
        print(f"Intentando URL {tipo_url}: {url}")
        soup = get_html_body(url)
        if soup is not None:
            print(f"HTML obtenido correctamente desde URL {tipo_url}: {url}")
            return soup

    raise RuntimeError("No se pudo obtener HTML de ninguna URL.")