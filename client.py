import requests
import io
from PIL import Image

SERVER_URL = "http://127.0.0.1:5000"

def request_generation():
    response = requests.get(f"{SERVER_URL}/generate")
    if response.status_code != 200:
        print("Failed to get response:", response.json())
        return
    
    data = response.json()
    print(f"Title: {data['title']}")
    print(f"Prompt: {data['prompt']}")
    
    image_url = f"{SERVER_URL}{data['image']}"
    image_response = requests.get(image_url)
    
    if image_response.status_code == 200:
        image = Image.open(io.BytesIO(image_response.content))
        image.show()
    else:
        print("Failed to fetch image")

if __name__ == "__main__":
    request_generation()
