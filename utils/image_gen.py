# utils/image_gen.py
import requests
import io
import time
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/SG161222/RealVisXL_V4.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

def generate_image(prompt: str, output_path: str, retries: int = 5, wait: int = 10) -> str:
    payload = {"inputs": prompt}
    for attempt in range(retries):
        response = query(payload)
        
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            image = Image.open(io.BytesIO(response.content))
            image.save(output_path)
            return output_path
        elif response.status_code == 503 and "Model is currently loading" in response.text:
            wait_time = wait * (2 ** attempt)  # Exponential backoff
            print(f"Model is loading, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            raise Exception(f"Image generation failed: {response.status_code}, {response.content.decode('utf-8')}")
    raise Exception(f"Image generation failed after {retries} retries")