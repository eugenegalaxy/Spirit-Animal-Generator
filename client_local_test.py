import requests
import io
from PIL import Image

SERVER_URL = "http://localhost"

def request_generation():
    try:
        response = requests.get(f"{SERVER_URL}/generate")
        if response.status_code != 200:
            print(f"Server error (status code {response.status_code})")
            print("Response content:", response.text)
            return
        
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Server did not return valid JSON")
            print("Response content:", response.text)
            return
        
        print(f"Title: {data['title']}")
        print(f"Prompt: {data['prompt']}")
        
        image_url = f"{SERVER_URL}{data['image']}"
        image_response = requests.get(image_url)
        
        if image_response.status_code == 200:
            image = Image.open(io.BytesIO(image_response.content))
            image.show()
        else:
            print("Failed to fetch image")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    request_generation()
