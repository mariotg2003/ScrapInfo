from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

from functions.insert_data import insert_data


def test_insert_data_writes_cleaned_values_to_database():
    engine = create_engine("sqlite:///:memory:")
    table = Table(
        "products",
        MetaData(),
        Column("id", Integer, primary_key=True),
        Column("product_name", String),
        Column("product_link", String),
        Column("product_price", String),
        Column("product_type", String),
        Column("product_img", String),
        Column("product_old_price", String),
    )
    table.create(engine)

    insert_data("Café", "https://example.com/café", "10", "gpu", "image", None, engine, table)

    with engine.connect() as connection:
        row = connection.execute(table.select()).one()

    assert row.product_name == "Café"
    assert row.product_link == "https://example.com/café"
    assert row.product_price == "10"
