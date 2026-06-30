from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from datetime import datetime
from dotenv import load_dotenv

def create_engine():

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

    return engine, products