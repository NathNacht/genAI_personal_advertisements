from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from faker import Faker
import schema as schema

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./utils/test.db')

Base = schema.Base
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)

def determine_persona(age, children):
    if age >= 60:
        return "seniors"
    elif age < 40 and not children:
        return "young adults"
    elif children and age <= 40:
        return "young family"
    elif children and age > 40:
        return "teenage family"
    else:
        return "other"  # This is a fallback for any edge cases

# Function to generate fake data
def create_fake_data():
    db = SessionLocal()
    fake = Faker()

    # Clear existing data
    db.query(schema.Customer).delete()
    db.query(schema.Subscription).delete()
    db.query(schema.Promotion).delete()
    db.query(schema.Channel).delete()
    db.query(schema.Persona).delete()
    db.query(schema.Advertisement).delete()
    db.query(schema.Outcome).delete()
    db.commit()

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

    # Create channels
    channels = [
        {"channel": "Web"},
        {"channel": "Email"},
        {"channel": "Social Media"},
        {"channel": "Magazine"},
        {"channel": "Billboard"}
    ]
    for ch in channels:
        db.add(schema.Channel(channel=ch["channel"]))

    # Create personas
    personas = [
        {"description": "young adults"},
        {"description": "young family"},
        {"description": "teenage family"},
        {"description": "seniors"},
        {"description": "other"}
    ]
    for persona in personas:
        db.add(schema.Persona(description=persona["description"]))

    db.commit()
    
    # Get persona IDs
    persona_dict = {persona.description: persona.id for persona in db.query(schema.Persona).all()}

    # Create customers
    subscription_ids = [sub.id for sub in db.query(schema.Subscription.id).all()]
    for _ in range(100):
        age = fake.random_int(min=18, max=80)
        married = fake.boolean()
        children = fake.boolean()
        persona_desc = determine_persona(age, children)
        persona_id = persona_dict.get(persona_desc, persona_dict["other"])
        
        customer = schema.Customer(
            name=fake.name(),
            age=age,
            city=fake.city(),
            country=fake.country(),
            married=married,
            children=children,
            pets=fake.random_int(min=0, max=3),
            subscription_id=fake.random_element(elements=subscription_ids),
            persona_id=persona_id
        )
        db.add(customer)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    print("Creating fake data...")
    create_fake_data()
    print("Fake data created successfully.")