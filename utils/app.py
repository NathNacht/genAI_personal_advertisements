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

def get_customer_details(customer_id):
    try:
        response = requests.get(f"{API_URL}/customer/{customer_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch customer details: {e}")
        return None

def generate_advertisement(customer_id, promotion_id, positive_prompt, negative_prompt, parameters):
    try:
        response = requests.post(
            f"{API_URL}/advertisement/{customer_id}",
            json={
                "promotion_id": promotion_id,
                "positive_prompt": positive_prompt,
                "negative_prompt": negative_prompt,
                "parameters": parameters,  # Changed to 'parameters' to match the FastAPI endpoint
            }
        )
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
    user_positive_prompt = st.text_area("Enter Positive Prompt")
    negative_prompt = st.text_area("Enter Negative Prompt")

    if st.button("Generate Advertisement"):
        customer_id = selected_customer.split(":")[0]
        promotion_id = selected_promotion.split(":")[0]

        # Fetch customer details
        customer_details = get_customer_details(customer_id)
        if customer_details:
            # Construct the positive prompt
            persona = customer_details.get("persona")
            country = customer_details.get("country")
            positive_prompt = f"{persona}, {country}, {user_positive_prompt}"
            parameters = {
                "negative_prompt": negative_prompt,
                "width": 1080,
                "height": 720,
                "steps": 100,
                "sampler": "DPM++ 3M SDE",
                "cfg_scale": 3.5,
                "clip_skip": 3,
                "hires_fix": {
                    "enabled": True,
                    "sampler": "DPM++ 3M SDE",
                    "steps": 50,
                    "strength": 0.2,
                    "upscale": 1.5,
                    "upscaler": "4x-UltraSharp"
                }
            }

            # Generate advertisement
            ad_info = generate_advertisement(customer_id, promotion_id, positive_prompt, negative_prompt, parameters)
        
            if ad_info:
                st.image(ad_info['generated_image_path'], caption='Generated Advertisement')
                st.write(f"Positive Prompt: {ad_info['positive_prompt']}")
                st.write(f"Negative Prompt: {ad_info['negative_prompt']}")
                st.write(f"Prompt Parameters: {ad_info['prompt_parameters']}")
            else:
                st.error("Failed to generate advertisement")
else:
    st.warning("No customers or promotions available.")