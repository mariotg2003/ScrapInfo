from bs4 import BeautifulSoup

from functions.format_data import parser_data


def test_parser_data_extracts_product_fields_and_optional_old_price():
    html = BeautifulSoup(
        """
        <div class="products">
          <a class="product" data-product-name="GPU" data-product-price="399.99" href="/gpu">
            <div class="images"><div class="source"><img src="/gpu.jpg"></div></div>
            <div class="price"><span class="discount">449.99</span></div>
          </a>
          <a class="product" data-product-name="CPU" data-product-price="199.99" href="/cpu">
            <div class="images"><div class="source"><img src="/cpu.jpg"></div></div>
          </a>
        </div>
        """,
        "html.parser",
    )
    params = {
        "clases_objetos": {
            "div_class_general": "products",
            "div_objetos": "product",
            "div_imagenes": "images",
            "div_src": "source",
            "div_precio": "price",
            "div_descuento": "discount",
        }
    }

    result = parser_data(html, "graphics", params)

    assert result == [
        {
            "name": "GPU",
            "link": "/gpu",
            "price": "399.99",
            "type": "graphics",
            "img": "/gpu.jpg",
            "old_price": "449.99",
        },
        {
            "name": "CPU",
            "link": "/cpu",
            "price": "199.99",
            "type": "graphics",
            "img": "/cpu.jpg",
            "old_price": None,
        },
    ]
