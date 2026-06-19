import argparse
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("API key missing")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot prompt")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=args.user_prompt,
)
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if not prompt_tokens or not response_tokens:
    raise RuntimeError("API request failed")
print(f"Prompt tokens: {prompt_tokens}")
print(f"Response tokens: {response_tokens}")
print(response.text)


def main():
    print("Hello from personal-ai-agent!")


if __name__ == "__main__":
    main()
