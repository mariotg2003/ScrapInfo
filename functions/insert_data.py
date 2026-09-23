from sqlalchemy.exc import OperationalError


def clean_data(text):
    if text is None: return ""
    return str(text).encode('utf-8','replace').decode('utf-8')


def insert_data(name, link, price, type, img, old_price, engine, table, retries=2):
    name = clean_data(name)
    link = clean_data(link)

    query = table.insert().values(
        product_name = name,
        product_link = link,
        product_price = price,
        product_type = type,
        product_img = img,
        product_old_price = old_price
    )

    # Reintenta una vez ante caídas de conexión SSL transitorias
    for attempt in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(query)
                conn.commit()
            return
        except OperationalError:
            if attempt == retries - 1:
                raise