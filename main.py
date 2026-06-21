import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("API key missing")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot prompt")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)


prompt_tokens: int | None = response.usage_metadata.prompt_token_count
response_tokens: int | None = response.usage_metadata.candidates_token_count

if not prompt_tokens or not response_tokens:
    raise RuntimeError("API request failed")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
print(response.text)


def main():
    print("Hello from personal-ai-agent!")


if __name__ == "__main__":
    main()
