# utils/schema.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    married = Column(Boolean)
    children = Column(Integer)
    pets = Column(Integer)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String)
    features = Column(String)
    price = Column(Integer)

class Promotion(Base):
    __tablename__ = 'promotions'
    id = Column(Integer, primary_key=True, index=True)
    details = Column(String)
    validity_period = Column(String)

class Advertisement(Base):
    __tablename__ = 'advertisements'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    promotion_id = Column(Integer, ForeignKey('promotions.id'))
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    generated_prompt = Column(Text)
    generated_image_path = Column(String)
    generated_text = Column(Text)
    outcome = Column(Boolean, default=None)

class Outcome(Base):
    __tablename__ = 'outcomes'
    id = Column(Integer, primary_key=True, index=True)
    ad_id = Column(Integer, ForeignKey('advertisements.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    timestamp = Column(String)
    action = Column(String)