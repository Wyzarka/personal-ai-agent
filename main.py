import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main():
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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt, temperature=0
        ),
    )

    prompt_tokens: int | None = response.usage_metadata.prompt_token_count
    response_tokens: int | None = response.usage_metadata.candidates_token_count

    if not prompt_tokens or not response_tokens:
        raise RuntimeError("API request failed")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    function_call_result = call_function(
        response.function_calls[0], verbose=args.verbose
    )
    if not function_call_result.parts:
        raise Exception("Function call failed")
    if not function_call_result.parts[0].function_response:
        raise Exception("Function call failed")
    if not function_call_result.parts[0].function_response.response:
        raise Exception("Function call failed")

    function_results = []
    function_results.append(function_call_result.parts[0].function_response.response)
    if args.verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(f"-> {function_call.name}({function_call.args})")


# def main():
#    print("Hello from personal-ai-agent!")


if __name__ == "__main__":
    main()
