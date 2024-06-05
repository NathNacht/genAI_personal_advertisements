from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os

load_dotenv()

# Set DATABASE_URL to save the database in the utils folder
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./utils/test.db')

Base = declarative_base()

class Advertisement(Base):
    __tablename__ = "advertisements"
    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer)
    promotion_id = Column(Integer, ForeignKey('promotions.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    positive_prompt = Column(Text)
    negative_prompt = Column(Text)
    prompt_parameters = Column(Text)
    generated_image_path = Column(String)
    outcome = Column(Boolean)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    married = Column(Boolean)
    children = Column(Boolean)
    pets = Column(Boolean)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    persona_id = Column(Integer, ForeignKey('personas.id'))

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String)
    features = Column(String)
    price = Column(Integer)

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True)
    details = Column(String)
    start = Column(Date)
    end = Column(Date)

class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True, index=True)
    persona = Column(Text)
    description = Column(Text)

class Outcome(Base):
    __tablename__ = "outcomes"
    id = Column(Integer, primary_key=True, index=True)
    ad_id = Column(Integer, ForeignKey('advertisements.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    timestamp = Column(String)
    action = Column(String)

# Database session and engine setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)