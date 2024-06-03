# utils/dummy_data.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from faker import Faker
import utils.schema as schema

# Load environment variables
load_dotenv()

# Ensure the utils directory exists
os.makedirs("utils", exist_ok=True)

# Set DATABASE_URL to save the database in the utils folder
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./utils/test.db')

Base = schema.Base
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)

# Function to generate fake data
def create_fake_data():
    db = SessionLocal()
    fake = Faker()

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
        {"details": "Referral Savings", "validity_period": "2024-12-31"},
        {"details": "Free Trial", "validity_period": "2024-12-31"},
        {"details": "Upgrade and Save", "validity_period": "2024-12-31"},
        {"details": "Downgrade and Save", "validity_period": "2024-12-31"},
        {"details": "Bundle and Save", "validity_period": "2024-12-31"},
    ]
    for promo in promotions:
        db.add(schema.Promotion(details=promo["details"], validity_period=promo["validity_period"]))

    db.commit()
    
    # Create customers
    subscription_ids = db.query(schema.Subscription.id).all()
    for _ in range(100):
        customer = schema.Customer(
            name=fake.name(),
            age=fake.random_int(min=18, max=80),
            city=fake.city(),
            country=fake.country(),
            married=fake.boolean(),
            children=fake.random_int(min=0, max=5),
            pets=fake.random_int(min=0, max=3),
            subscription_id=fake.random_element(elements=subscription_ids)[0]
        )
        db.add(customer)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    create_fake_data()