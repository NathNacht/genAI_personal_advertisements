# add_advertisement_columns.py
from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

metadata = MetaData()
metadata.reflect(bind=engine)
advertisements_table = Table('advertisements', metadata, autoload_with=engine)

new_columns = {
    'promotion_details': Text,
    'media': String
}

for column_name, column_type in new_columns.items():
    if column_name not in [c.name for c in advertisements_table.columns]:
        try:
            with engine.connect() as conn:
                conn.execute(text(f'ALTER TABLE advertisements ADD COLUMN {column_name} {column_type.__name__}'))
                print(f"Column '{column_name}' added successfully.")
        except OperationalError as e:
            print(f"Error occurred: {e}")
    else:
        print(f"Column '{column_name}' already exists.")