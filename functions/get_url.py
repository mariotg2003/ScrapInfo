import cloudscraper
from bs4 import BeautifulSoup

def get_html_body(url: str):

    soup = None

    scraper = cloudscraper.create_scraper(
            delay=10,  # Espera un poco por si hay protecciones de Cloudflare
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )
    
    try: 

        scraper.get("https://www.pccomponentes.com/")

        response = scraper.get(url, timeout=30)

        if response.status_code == 200:

            htmlBody = response.text

            soup = BeautifulSoup(htmlBody, "html.parser")

        else:
            print(response.status_code)

    except Exception as e:
        print(e)

    return soup