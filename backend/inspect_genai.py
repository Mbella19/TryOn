from google import genai
import inspect

print("Google GenAI Version:", genai.__version__)
print("\nGenerateContentConfig fields:")
try:
    for field in genai.types.GenerateContentConfig.model_fields:
        print(f"- {field}")
except Exception as e:
    print(f"Error inspecting fields: {e}")

print("\nThinkingConfig fields:")
try:
    for field in genai.types.ThinkingConfig.model_fields:
        print(f"- {field}")
except Exception as e:
    print(f"Error inspecting ThinkingConfig: {e}")
