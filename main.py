# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/advertisement/{customer_id}")
def get_advertisement(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    subscription = db.query(models.Subscription).filter(models.Subscription.id == customer.subscription_id).first()
    promotion = db.query(models.Promotion).filter(models.Promotion.id == 1).first()  # Placeholder promotion
    
    generated_prompt = f"Special offer for {customer.name} with {subscription.plan_name} plan and promotion: {promotion.details}"
    generated_image_path = "/path/to/generated/image.png"
    generated_text = "Check out this amazing offer tailored just for you!"
    
    ad = models.Advertisement(
        customer_id=customer_id,
        promotion_id=promotion.id,
        subscription_id=customer.subscription_id,
        generated_prompt=generated_prompt,
        generated_image_path=generated_image_path,
        generated_text=generated_text
    )
    
    db.add(ad)
    db.commit()
    db.refresh(ad)
    
    return ad

@app.post("/advertisement/{ad_id}/action")
def advertisement_action(ad_id: int, action: str, db: Session = Depends(get_db)):
    ad = db.query(models.Advertisement).filter(models.Advertisement.id == ad_id).first()
    if ad is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    ad.outcome = True if action == "accept" else False
    db.commit()
    db.refresh(ad)
    
    outcome = models.Outcome(
        ad_id=ad.id,
        customer_id=ad.customer_id,
        timestamp="2024-06-03T00:00:00Z",
        action=action
    )
    db.add(outcome)
    db.commit()
    db.refresh(outcome)
    
    return {"status": "success", "outcome": outcome}