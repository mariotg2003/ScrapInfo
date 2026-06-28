import cloudscraper
from bs4 import BeautifulSoup

def get_html_body(url: str):

    scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        })
    response = scraper.get(url)

    if response.status_code == 200:

        htmlBody = response.text

        soup = BeautifulSoup(htmlBody, "html.parser")

    else:
        print(response.status_code)

    return soup