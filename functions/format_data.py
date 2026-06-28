from bs4 import BeautifulSoup


def parser_data(htmlBody, type, params):

    clases = params["clases_objetos"]

    div_principal = clases["div_class_general"]
    div_objeto = clases["div_objetos"]

    diccionarioObjetos = []

    divObjetos = htmlBody.find("div", class_=div_principal)

    productos = divObjetos.select("a", class_=div_objeto)

    for element in productos:

        titulo = element.get("data-product-name")
        enlace = element.get("href")
        precio = element.get("data-product-price")
    
        productoJson = {
            "name" : titulo,
            "link" : enlace,
            "price" : precio,
            "type" : type
        }


        diccionarioObjetos.append(productoJson)

    return diccionarioObjetos