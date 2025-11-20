import os
import sys
from dotenv import load_dotenv
from gemini_service import GeminiService

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ GOOGLE_API_KEY not found in environment")
    # Try to read from .env file directly if load_dotenv didn't work (e.g. if it's in a parent dir)
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('GOOGLE_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                    os.environ['GOOGLE_API_KEY'] = api_key
                    print("🔑 Loaded API KEY from manual .env read")
                    break
    except Exception as e:
        print(f"⚠️ Could not read .env manually: {e}")

if not api_key:
    print("❌ Still no API Key found. Exiting.")
    sys.exit(1)

print(f"🔑 API Key found: {api_key[:5]}...{api_key[-5:]}")

try:
    service = GeminiService(api_key)
    print("🚀 Testing generate_clothing_image...")
    img = service.generate_clothing_image("blue denim jacket")
    print("✅ Image generated successfully")
    img.save("debug_output.png")
    print("💾 Saved to debug_output.png")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
