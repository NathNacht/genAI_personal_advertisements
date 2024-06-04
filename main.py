# main.py
import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from utils import SessionLocal, engine, Customer, Subscription, Promotion, Advertisement, Outcome, generate_prompt, generate_image, Base
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

@app.get("/advertisement/{customer_id}")
def get_advertisement(customer_id: int, promotion_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching customer with ID {customer_id}")
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        logging.error(f"Customer with ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    logging.info(f"Fetching subscription with ID {customer.subscription_id}")
    subscription = db.query(Subscription).filter(Subscription.id == customer.subscription_id).first()
    logging.info(f"Fetching promotion with ID {promotion_id}")
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    
    if subscription is None or promotion is None:
        logging.error("Subscription or Promotion not found")
        raise HTTPException(status_code=404, detail="Subscription or Promotion not found")

    customer_details = (
        f"Name: {customer.name}, Age: {customer.age}, City: {customer.city}, "
        f"Country: {customer.country}, Married: {customer.married}, Children: {customer.children}, "
        f"Pets: {customer.pets}, Subscription: {subscription.plan_name}"
    )
    promotion_details = f"Promotion: {promotion.details}, Validity: {promotion.validity_period}"
    
    logging.info(f"Generating prompt with customer details: {customer_details} and promotion details: {promotion_details}")
    generated_prompt = generate_prompt(customer_details, promotion_details)
    
    # Ensure the image directory exists
    os.makedirs("images", exist_ok=True)
    
    # Generate the image based on the prompt
    image_path = f"images/customer_{customer_id}_ad.png"
    
    try:
        logging.info(f"Generating image with prompt: {generated_prompt}")
        generate_image(generated_prompt, image_path)
    except Exception as e:
        logging.error(f"Image generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")
    
    ad = Advertisement(
        customer_id=customer_id,
        promotion_id=promotion.id,
        subscription_id=customer.subscription_id,
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