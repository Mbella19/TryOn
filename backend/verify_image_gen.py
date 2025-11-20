import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_service import GeminiService

# Load environment variables
load_dotenv()

def test_image_generation():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        return

    service = GeminiService(api_key)
    
    print("🧪 Testing generate_clothing_image with gemini-3-pro-image-preview...")
    try:
        image = service.generate_clothing_image("A red t-shirt")
        if image:
            print("✅ Image generated successfully!")
            image.save("test_generated_clothing.png")
            print("Saved to test_generated_clothing.png")
        else:
            print("❌ Failed to generate image")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_image_generation()
