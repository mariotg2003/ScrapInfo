
def delete_data(engine, table):

    with engine.connect() as conn:
        conn.execute(table.delete())
        conn.commit()