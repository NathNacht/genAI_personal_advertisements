import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from utils import SessionLocal, engine, Customer, Subscription, Promotion, Channel, Advertisement, Outcome, generate_prompt, generate_image, Base
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers

@app.get("/promotions")
def get_promotions(db: Session = Depends(get_db)):
    promotions = db.query(Promotion).all()
    return promotions

@app.get("/channels")
def get_channels(db: Session = Depends(get_db)):
    channels = db.query(Channel).all()
    return channels

@app.get("/advertisement/{customer_id}/{channel_id}")
def get_advertisement(customer_id: int, channel_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    subscription = db.query(Subscription).filter(Subscription.id == customer.subscription_id).first()
    promotion = db.query(Promotion).filter(Promotion.id == 1).first()  # Placeholder promotion
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")

    customer_details = (
        f"Name: {customer.name}, Age: {customer.age}, City: {customer.city}, "
        f"Country: {customer.country}, Married: {customer.married}, Children: {customer.children}, "
        f"Pets: {customer.pets}, Subscription: {subscription.plan_name}"
    )
    promotion_details = f"Promotion: {promotion.details}, Validity: {promotion.validity_period}"
    channel_details = f"Channel: {channel.channel}"
    
    generated_prompt = generate_prompt(f"{customer_details}, {promotion_details}, {channel_details}")
    
    # Ensure the image directory exists
    os.makedirs("images", exist_ok=True)
    
    # Generate the image based on the prompt
    image_path = f"images/customer_{customer_id}_ad.png"
    
    try:
        generate_image(generated_prompt, image_path)
    except Exception as e:
        logging.error(f"Image generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")
    
    ad = Advertisement(
        customer_id=customer_id,
        promotion_id=promotion.id,
        subscription_id=customer.subscription_id,
        channel_id=channel.id,
        generated_prompt=generated_prompt,
        generated_image_path=image_path,
        generated_text=""  # This will be updated later
    )
    
    db.add(ad)
    db.commit()
    db.refresh(ad)
    
    return ad

@app.post("/advertisement/{ad_id}/action")
def advertisement_action(ad_id: int, action: str, db: Session = Depends(get_db)):
    ad = db.query(Advertisement).filter(Advertisement.id == ad_id).first()
    if ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    ad.outcome = True if action == "accept" else False
    db.commit()
    db.refresh(ad)
    
    outcome = Outcome(
        ad_id=ad.id,
        customer_id=ad.customer_id,
        timestamp="2024-06-03T00:00:00Z",
        action=action
    )
    db.add(outcome)
    db.commit()
    db.refresh(outcome)
    
    return {"status": "success", "outcome": outcome}