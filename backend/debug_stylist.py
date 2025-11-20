import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ GOOGLE_API_KEY not found in environment")
    exit(1)

print(f"Using API Key: {api_key[:5]}...")

client = genai.Client(api_key=api_key, http_options={'api_version': 'v1alpha'})

try:
    print("🤖 Testing Gemini 3 Pro Preview with High Thinking...")
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents="Suggest a dinner outfit for a cold evening in London.",
        config=genai.types.GenerateContentConfig(
            thinking_config=genai.types.ThinkingConfig(
                include_thoughts=True,
                thinking_level="HIGH"
            )
        )
    )
    print("✓ Success!")
    print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
