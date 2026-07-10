def clean_data(text):
    if text is None: return ""
    return str(text).encode('utf-8','replace').decode('utf-8')


def insert_data(name, link, price, type, img, engine, table):
    with engine.connect() as conn:

        name = clean_data(name)
        link = clean_data(link)

        query = table.insert().values(
            product_name = name,
            product_link = link,
            product_price = price,
            product_type = type,
            product_img = img
        )

        conn.execute(query)
        conn.commit()