import requests
import io
import time
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/Corcelio/mobius"
headers = {"Authorization": "Bearer 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"}

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
            "steps": 50,  # Recommended steps for quality and efficiency
            "sampler": "DPM++ 3M SDE",  # Recommended sampler
            "cfg_scale": 3.5,  # Recommended CFG scale for extreme realism
            "clip_skip": 3,  # Recommended CLIP skip
            "hires_fix": {
                "enabled": True,
                "sampler": "DPM++ 3M SDE",  # Recommended Hires.Fix sampler
                "steps": 50,  # Recommended denoising steps for Hires.Fix
                "strength": 0.2,  # Denoising strength for Hires.Fix
                "upscale": 1.5,  # Upscale factor for Hires.Fix
                "upscaler": "4x-UltraSharp"  # Recommended upscaler
            }
        }
    }
    for attempt in range(retries):
        response = query(payload)
        
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            image = Image.open(io.BytesIO(response.content))
            
            # Save the initial image
            image.save(output_path)
            
            # Apply ADetailer enhancements directly on the saved image
            final_image_path = apply_adetailer(output_path, output_path)
            return final_image_path
        
        elif response.status_code == 503 and "Model is currently loading" in response.text:
            wait_time = wait * (2 ** attempt)  # Exponential backoff
            print(f"Model is loading, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            raise Exception(f"Image generation failed: {response.status_code}, {response.content.decode('utf-8')}")
    
    raise Exception(f"Image generation failed after {retries} retries")

def apply_adetailer(input_image_path: str, output_image_path: str) -> str:
    # Load the initial image
    initial_image = Image.open(input_image_path)

    # Apply ADetailer enhancements (this is a placeholder for actual implementation)
    # For example, enhancing facial details, removing artifacts, etc.
    enhanced_image = initial_image  # Replace with actual ADetailer processing

    # Save the enhanced image
    enhanced_image.save(output_image_path)

    return output_image_path