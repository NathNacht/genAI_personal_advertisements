import requests
import io
import time
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/Corcelio/mobius"
api_token = os.getenv("HUGGINGFACE_API_TOKEN")
if not api_token:
    raise ValueError("No API token provided. Please set the HUGGINGFACE_API_TOKEN environment variable.")
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

def generate_image(positive_prompt: str, negative_prompt: str, output_path: str, retries: int = 10, wait: int = 30) -> str:
    payload = {
        "inputs": positive_prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "width": 512,
            "height": 512,
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
    }
    for attempt in range(retries):
        response = query(payload)
        
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            image = Image.open(io.BytesIO(response.content))
            image.save(output_path)
            final_image_path = apply_adetailer(output_path, output_path)
            return final_image_path
        
        elif response.status_code == 503 and "Model is currently loading" in response.text:
            wait_time = wait * (2 ** attempt)
            print(f"Model is loading, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            raise Exception(f"Image generation failed: {response.status_code}, {response.content.decode('utf-8')}")
    
    raise Exception(f"Image generation failed after {retries} retries")

def apply_adetailer(input_image_path: str, output_image_path: str) -> str:
    initial_image = Image.open(input_image_path)
    enhanced_image = initial_image
    enhanced_image.save(output_image_path)
    return output_image_path