import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_customers():
    try:
        response = requests.get(f"{API_URL}/customers")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch customers: {e}")
        return []

def get_promotions():
    try:
        response = requests.get(f"{API_URL}/promotions")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch promotions: {e}")
        return []

def generate_advertisement(customer_id, promotion_id):
    try:
        response = requests.get(f"{API_URL}/advertisement/{customer_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to generate advertisement: {e}")
        return None

# Streamlit UI
st.title("Advertisement Generator")

customers = get_customers()
promotions = get_promotions()

if customers and promotions:
    customer_names = [f"{cust['id']}: {cust['name']}" for cust in customers]
    promotion_details = [f"{promo['id']}: {promo['details']}" for promo in promotions]

    selected_customer = st.selectbox("Select Customer", customer_names)
    selected_promotion = st.selectbox("Select Promotion", promotion_details)

    if st.button("Generate Advertisement"):
        customer_id = selected_customer.split(":")[0]
        promotion_id = selected_promotion.split(":")[0]
        ad_info = generate_advertisement(customer_id, promotion_id)
        
        if ad_info:
            st.image(ad_info['generated_image_path'], caption='Generated Advertisement')
            st.write(f"Prompt: {ad_info['generated_prompt']}")
        else:
            st.error("Failed to generate advertisement")