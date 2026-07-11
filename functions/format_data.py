from bs4 import BeautifulSoup


def parser_data(htmlBody, type, params):

    clases = params["clases_objetos"]

    div_principal = clases["div_class_general"]
    div_objeto = clases["div_objetos"]
    div_imagenes = clases["div_imagenes"]
    div_src = clases["div_src"]
    div_precio = clases["div_precio"]
    div_descuento = clases["div_descuento"]

    diccionarioObjetos = []

    divObjetos = htmlBody.find("div", class_=div_principal)
    
    productos = divObjetos.select("a", class_=div_objeto)

    for element in productos:

        div_img = element.find("div", class_=div_imagenes) 
        price_div = element.find("div", class_=div_precio) if element.find("div", class_=div_precio) else None

        if price_div is not None:
            old_price = price_div.find("span", class_=div_descuento).text if price_div.find("span", class_=div_descuento) else None
        else:
            old_price = None
        
        img_source = div_img.find("div", class_=div_src)
        img_tag = img_source.find("img")

        img = img_tag.get("src")
        titulo = element.get("data-product-name")
        enlace = element.get("href")
        precio = element.get("data-product-price")


        productoJson = {
            "name" : titulo,
            "link" : enlace,
            "price" : precio,
            "type" : type,
            "img" : img,
            "old_price" : old_price
        }


        diccionarioObjetos.append(productoJson)

    return diccionarioObjetos