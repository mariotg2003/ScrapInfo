import pytest
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, select
from sqlalchemy.exc import IntegrityError

from atomic_update import replace_products


@pytest.fixture
def database():
    engine = create_engine("sqlite://")
    metadata = MetaData()
    table = Table(
        "Object", metadata,
        Column("id", Integer, primary_key=True),
        Column("product_name", String, nullable=False),
        Column("product_link", String),
        Column("product_price", String),
        Column("product_type", String),
        Column("product_img", String),
        Column("product_old_price", String),
    )
    metadata.create_all(engine)
    with engine.begin() as connection:
        connection.execute(table.insert(), [{"product_name": "original"}])
    return engine, table


def names(database):
    engine, table = database
    with engine.connect() as connection:
        return connection.execute(select(table.c.product_name)).scalars().all()


def product(name):
    return {"name": name, "link": "link", "price": "1", "type": "x", "img": "", "old_price": None}


def test_replaces_only_after_every_page_succeeds(database):
    engine, table = database
    params = {"paginas": {"a": {"url": "a"}, "b": {"url": "b"}}}

    def parse(body, _kind, _params):
        if body == "b":
            raise ValueError("parse failed")
        return [product("new")]

    with pytest.raises(ValueError, match="parse failed"):
        replace_products(engine, table, params, lambda urls: urls[0], parse, str)
    assert names(database) == ["original"]

    count = replace_products(engine, table, params, lambda urls: urls[0], lambda body, *_: [product(body)], str)
    assert count == 2
    assert names(database) == ["a", "b"]


def test_rolls_back_delete_when_insert_fails(database):
    engine, table = database
    params = {"paginas": {"a": {"url": "a"}}}
    bad = product("new")
    bad["type"] = None
    del bad["img"]
    with pytest.raises(KeyError):
        replace_products(engine, table, params, lambda urls: urls[0], lambda *_: [bad], str)
    assert names(database) == ["original"]

    bad = product(None)
    with pytest.raises(IntegrityError):
        replace_products(engine, table, params, lambda urls: urls[0], lambda *_: [bad], lambda value: value)
    assert names(database) == ["original"]


def test_empty_pages_or_empty_results_preserve_data(database):
    engine, table = database
    for params in ({"paginas": {}}, {"paginas": {"a": {"url": "a"}}}):
        with pytest.raises(ValueError):
            replace_products(engine, table, params, lambda urls: urls[0], lambda *_: [], str)
        assert names(database) == ["original"]
