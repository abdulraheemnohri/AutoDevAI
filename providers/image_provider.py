import requests
import random
import os
import urllib.parse
from datetime import datetime

def generate_image(prompt, save_path="images", width=1080, height=1920, enhance=True):
    """Generate an image using Pollinations AI."""
    params = {
        "safe": True,
        "seed": random.randint(1, 999999999),
        "width": width,
        "height": height,
        "nologo": True,
        "private": True,
        "model": "flux",
        "enhance": enhance,
        "referrer": "autodevai"
    }
    encoded_prompt = urllib.parse.quote(prompt)
    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?{query}"

    try:
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(save_path, f"img_{timestamp}.png")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"🎨 Image generated and saved to: {path}")
            return path
        else:
            print(f"❌ Image generation failed with status code: {r.status_code}")
            return None
    except Exception as e:
        print(f"❌ Image generation error: {e}")
        return None
