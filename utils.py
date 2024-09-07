from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import requests
import torch

model_id = "vikhyatk/moondream2"
revision = "2024-07-23"
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision,
                                             do_sample=True, temperature=0.9,top_p=0.9,top_k=40)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

def process_single_image_and_get_result(image, prompt="Define the image"):
    # No need to open the image again, it's already opened and passed as an image object
    image = image.convert('RGB')  # Ensure it's in RGB format
    enc_image = model.encode_image(image)
    result = model.answer_question(enc_image, prompt, tokenizer)
    print("results created")
    return result

