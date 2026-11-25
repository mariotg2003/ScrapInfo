def replace_products(engine, table, params, get_html_body, parser_data, clean_data):
    pages = params["paginas"]
    if not pages:
        raise ValueError("No hay páginas configuradas; no se modificará la base de datos.")

    products = []
    for product_type, page in pages.items():
        urls = [page["url"]]
        fallback = page.get("url_respaldo", "").strip()
        if fallback:
            urls.append(fallback)
        found = parser_data(get_html_body(urls), product_type, params)
        if not found:
            raise ValueError(f"No se encontraron productos para {product_type}; no se modificará la base de datos.")
        print(f"Preparando {len(found)} objetos {product_type}")
        for item in found:
            products.append({
                "product_name": clean_data(item["name"]),
                "product_link": clean_data(item["link"]),
                "product_price": item["price"],
                "product_type": item["type"],
                "product_img": item["img"],
                "product_old_price": item["old_price"],
            })

    with engine.begin() as connection:
        if engine.dialect.name == "postgresql":
            table_name = engine.dialect.identifier_preparer.format_table(table)
            connection.exec_driver_sql(f"LOCK TABLE {table_name} IN EXCLUSIVE MODE")
        connection.execute(table.delete())
        connection.execute(table.insert(), products)
    return len(products)
