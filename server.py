from flask import Flask, jsonify, send_file
import os
import random
import time
import torch
from diffusers import StableDiffusionPipeline
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=["50 per hour"])

CHIMERA_CHANCE = 0.1
WORDS_DIR = os.path.join(os.path.dirname(__file__), 'words')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images')

STABLE_DIFFUSION_MODEL_ID = "runwayml/stable-diffusion-v1-5"
STABLE_DIFFUSION_NUM_STEPS = 40
STABLE_DIFFUSION_GUIDANCE_SCALE = 12


if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def get_random_word_from_file(file_path):
    """Reads a file and returns a random word or phrase from it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            phrases = [phrase.strip() for phrase in file.read().split(',')]
            phrases = [phrase for phrase in phrases if phrase]  # Remove empty strings
            return random.choice(phrases) if phrases else None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def generate_prompt():
    """Generates a prompt and a name."""
    if not os.path.exists(WORDS_DIR):
        return None, None
    
    # Chimera chance
    if random.random() < CHIMERA_CHANCE:
        animal1 = get_random_word_from_file(os.path.join(WORDS_DIR, 'animals.txt')) or "mystical creature"
        animal2 = get_random_word_from_file(os.path.join(WORDS_DIR, 'animals.txt')) or "legendary beast"
        animal_description = f"{animal1}-{animal2} chimera"
    else:
        animal_description = get_random_word_from_file(os.path.join(WORDS_DIR, 'animals.txt')) or "mystical creature"
    
    adjective = get_random_word_from_file(os.path.join(WORDS_DIR, 'adjectives.txt')) or "mysterious"
    symbolism = get_random_word_from_file(os.path.join(WORDS_DIR, 'symbolism.txt')) or "wanders"
    name = f"{adjective.title()} {animal_description.title()} of {symbolism.title()}"
    
    files = [f for f in os.listdir(WORDS_DIR) if f.endswith('.txt') and f != 'animals.txt']
    words = [get_random_word_from_file(os.path.join(WORDS_DIR, file)) for file in files]
    words = [word for word in words if word]  # Remove None values
    
    general_style = get_random_word_from_file(os.path.join(WORDS_DIR, 'general_style.txt')) or "Highly detailed illustration"

    prompt = f"{general_style} of a {animal_description}, with natural anatomy, " + ', '.join(words)
    
    return prompt, name

def generate_image(prompt):
    """Generates an image and returns its filename."""
    model_id = STABLE_DIFFUSION_MODEL_ID
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None, local_files_only=True).to("cuda")
    pipe.enable_xformers_memory_efficient_attention()
    pipe.enable_attention_slicing()
    image = pipe(prompt, num_inference_steps=STABLE_DIFFUSION_NUM_STEPS, guidance_scale=STABLE_DIFFUSION_GUIDANCE_SCALE).images[0]
    filename = f"image_{int(time.time())}.png"
    image_path = os.path.join(IMAGES_DIR, filename)
    image.save(image_path)
    return filename

@app.route('/generate', methods=['GET'])
@limiter.limit("5 per minute")  # 5 requests per minute per IP
def generate():
    prompt, name = generate_prompt()
    if not prompt:
        return jsonify({"error": "Failed to generate prompt"}), 500
    
    image_filename = generate_image(prompt)
    
    return jsonify({
        "title": name,
        "prompt": prompt,
        "image": f"/images/{image_filename}"
    })

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    image_path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(image_path):
        response = jsonify({"error": "Image not found"})
        response.status_code = 404
        return response
    response = send_file(image_path, mimetype='image/png')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)