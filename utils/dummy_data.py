from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from faker import Faker
import schema as schema
from schema import SessionLocal, engine, Base  # Import SessionLocal, engine, and Base from schema
from datetime import datetime

# Load environment variables
load_dotenv()

# Create the tables
Base.metadata.drop_all(bind=engine)  # Drop existing tables
Base.metadata.create_all(bind=engine)  # Create new tables

# Persona dictionary
persona_dict = {
    1: ("Young Adult", "single, young adult"),
    2: ("Young Family", "two parents with young children"),
    3: ("Teenage Family", "two parents with teenage children"),
    4: ("Senior", "retired and free"),
    5: ("Other", "middle aged")
}

# List of specified countries
country_list = [
    "Botswana", "Burkina Faso", "Cameroon", "Egypt", "Guinea Bissau", "Guinea Conakry", "Ivory Coast", "Jordan",
    "Liberia", "Madagascar", "Mali", "Mauritius", "Morocco", "Centrafrican Republic", "Democratic Republic of Congo",
    "Senegal", "Sierra Leone", "Tunisia", "Belgium", "France", "Luxembourg", "Moldova", "Poland", "Roumania",
    "Slovakia", "Spain"
]

# Function to generate fake data
def create_fake_data():
    db = SessionLocal()
    fake = Faker()

    # Create personas
    for id, (persona, description) in persona_dict.items():
        db.add(schema.Persona(id=id, persona=persona, description=description))

    # Create subscriptions
    subscriptions = [
        {"plan_name": "Go Light", "features": "Basic features", "price": 10},
        {"plan_name": "Go Plus", "features": "Standard features", "price": 20},
        {"plan_name": "Go Intense", "features": "Advanced features", "price": 30},
        {"plan_name": "Go Extreme", "features": "All features", "price": 40},
    ]
    for sub in subscriptions:
        db.add(schema.Subscription(plan_name=sub["plan_name"], features=sub["features"], price=sub["price"]))

    # Create promotions
    promotions = [
        {"details": "Referral Savings", "start": datetime.strptime("2023-01-01", "%Y-%m-%d"), "end": datetime.strptime("2024-12-31", "%Y-%m-%d")},
        {"details": "Free Trial", "start": datetime.strptime("2023-01-01", "%Y-%m-%d"), "end": datetime.strptime("2024-12-31", "%Y-%m-%d")},
        {"details": "Upgrade and Save", "start": datetime.strptime("2023-01-01", "%Y-%m-%d"), "end": datetime.strptime("2024-12-31", "%Y-%m-%d")},
        {"details": "Downgrade and Save", "start": datetime.strptime("2023-01-01", "%Y-%m-%d"), "end": datetime.strptime("2024-12-31", "%Y-%m-%d")},
        {"details": "Bundle and Save", "start": datetime.strptime("2023-01-01", "%Y-%m-%d"), "end": datetime.strptime("2024-12-31", "%Y-%m-%d")},
    ]
    for promo in promotions:
        db.add(schema.Promotion(details=promo["details"], start=promo["start"], end=promo["end"]))

    db.commit()

    # Create customers
    subscription_ids = [sub.id for sub in db.query(schema.Subscription.id).all()]
    for _ in range(100):
        age = fake.random_int(min=18, max=80)
        children = fake.boolean()
        persona_id = 1 if age < 40 and not children else 2 if age < 40 and children else 3 if age > 40 and children else 4 if age > 60 else 5

        customer = schema.Customer(
            name=fake.name(),
            age=age,
            city=fake.city(),
            country=fake.random_element(elements=country_list),
            married=fake.boolean(),
            children=children,
            pets=fake.boolean(),
            subscription_id=fake.random_element(elements=subscription_ids),
            persona_id=persona_id
        )
        db.add(customer)

    db.commit()
    db.close()

if __name__ == "__main__":
    create_fake_data()