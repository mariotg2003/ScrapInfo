from bs4 import BeautifulSoup
from typing import Optional


from functions.get_url import get_html_body
from functions.format_data import parser_data
from functions.read_params import get_info
from functions.create_json import write_json
from functions.insert_data import insert_data
from functions.delete_data import delete_data
from functions.send_email import send_email


if __name__ == "__main__":

    # Borrado de tablas
    delete_data()

    # Leer JSON
    params_exe = get_info("pcComponentesData")
    paginas = params_exe["paginas"]
    execution = False

    for element in paginas:

        url = paginas[element]["url"]
        body_html = get_html_body(url)
        dic_objets = parser_data(body_html, element, params_exe)

        for element_objects in dic_objets:

            element_name = element_objects['name']
            element_link = element_objects['link']
            element_price = element_objects['price']
            element_type = element_objects['type']

            try:
                insert_data(element_name,element_link,element_price,element_type)
                execution = True
            except Exception as e:
                execution = False
                print(f"error al subir los datos {e}")

    if execution : 
        send_email("Exitosa")
    else:
        send_email("Fallida")
