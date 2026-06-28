from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")

engine = create_engine(os.getenv("DATABASE_URL"), connect_args={"options": "-c client_encoding=utf8"})
metadata = MetaData()


products = Table("Object", metadata, 
    Column('id', Integer, primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('product_name', String),
    Column('product_link', String),
    Column('product_price', String),
    Column('product_type', String),       
)

def clean_data(text):
    if text is None: return ""
    return str(text).encode('utf-8','replace').decode('utf-8')


def insert_data(name, link, price, type):
    with engine.connect() as conn:

        name = clean_data(name)
        link = clean_data(link)

        query = products.insert().values(
            product_name = name,
            product_link = link,
            product_price = price,
            product_type = type
        )

        conn.execute(query)
        conn.commit()