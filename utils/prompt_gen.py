from transformers import pipeline

# Load a pre-trained text generation model (e.g., GPT-2)
generator = pipeline("text-generation", model="gpt2")  # Replace "gpt2" with the actual model name if needed

def generate_prompt(customer_details: str, promotion_details: str) -> str:
    prompt = (
        f"Generate a hyperrealistic photograph description for a promotional image based on the following details:\n"
        f"Customer Details: {customer_details["persona"]}\n"
        f"Promotion Details: {promotion_details}\n"
        f"Description: "
    )
    result = generator(prompt, max_length=200, num_return_sequences=1)
    generated_text = result[0]['generated_text']
    
    # Remove any unexpected artifacts in the generated text
    if "Cameo:" in generated_text:
        generated_text = generated_text.split("Cameo:")[0].strip()
    
    return generated_text