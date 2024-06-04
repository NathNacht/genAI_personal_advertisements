import requests
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/SG161222/RealVisXL_V4.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

def generate_image(prompt: str, output_path: str) -> str:
    payload = {"inputs": prompt}
    response = query(payload)
    
    if response.status_code == 500:
        # Retry with potential optimizations
        print("Retrying with CPU...")
        payload = {
            "inputs": prompt,
            "options": {"use_cpu": True}  # Example if API supports CPU usage
        }
        response = query(payload)
    
    if response.status_code == 200 and 'image' in response.headers['Content-Type']:
        image = Image.open(io.BytesIO(response.content))
        image.save(output_path)
        return output_path
    else:
        raise Exception(f"Image generation failed: {response.status_code}, {response.content.decode('utf-8')}")