from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Boolean, ForeignKey, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

metadata = MetaData()
metadata.reflect(bind=engine)

# Define the new advertisements table structure without the unwanted columns
new_advertisements_table = Table(
    'advertisements_new', metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('promotion_id', Integer, ForeignKey('promotions.id')),
    Column('subscription_id', Integer),
    Column('generated_image_path', String),
    Column('outcome', Boolean),
    Column('negative_prompt', Text),
    Column('prompt_parameters', Text)  # New column
)

# Define the personas table with the new description column
personas_table = Table('personas', metadata, autoload_with=engine)
if 'description' not in [c.name for c in personas_table.columns]:
    with engine.connect() as conn:
        conn.execute(text('ALTER TABLE personas ADD COLUMN description VARCHAR'))

# Create the new advertisements table
with engine.connect() as conn:
    try:
        new_advertisements_table.create(bind=engine)
        print("New table 'advertisements_new' created successfully.")
    except OperationalError as e:
        print(f"Error occurred while creating new table: {e}")

# Copy data from the old advertisements table to the new table
with engine.connect() as conn:
    try:
        conn.execute(text("""
            INSERT INTO advertisements_new (id, customer_id, promotion_id, subscription_id, generated_image_path, outcome, negative_prompt)
            SELECT id, customer_id, promotion_id, subscription_id, generated_image_path, outcome, negative_prompt
            FROM advertisements;
        """))
        print("Data copied to new table 'advertisements_new' successfully.")
    except OperationalError as e:
        print(f"Error occurred while copying data: {e}")

# Drop the old advertisements table
with engine.connect() as conn:
    try:
        conn.execute(text("DROP TABLE advertisements;"))
        print("Old table 'advertisements' dropped successfully.")
    except OperationalError as e:
        print(f"Error occurred while dropping old table: {e}")

# Rename the new advertisements table to the original name
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE advertisements_new RENAME TO advertisements;"))
        print("New table renamed to 'advertisements' successfully.")
    except OperationalError as e:
        print(f"Error occurred while renaming new table: {e}")

# Update the personas table with descriptions
persona_dict = {
    1: "single, young adult",
    2: "two parents with young children",
    3: "two parents with teenage children",
    4: "retired and free",
    5: "middle aged"
}

with engine.connect() as conn:
    for persona_id, description in persona_dict.items():
        try:
            conn.execute(text(f"UPDATE personas SET description = :description WHERE id = :id"), {'description': description, 'id': persona_id})
            print(f"Updated persona id {persona_id} with description '{description}'")
        except OperationalError as e:
            print(f"Error occurred while updating persona id {persona_id}: {e}")