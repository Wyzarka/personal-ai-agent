import argparse
import os
import sys

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

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    max_iterations = 20
    for iteration in range(max_iterations):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        prompt_tokens: int | None = response.usage_metadata.prompt_token_count
        response_tokens: int | None = response.usage_metadata.candidates_token_count

        if not prompt_tokens or not response_tokens:
            raise RuntimeError("API request failed")

        if args.verbose:
            print(f"Iteration {iteration + 1}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

        candidates = response.candidates or []
        for candidate in candidates:
            if candidate.content:
                messages.append(candidate.content)

        function_responses: list[types.Part] = []
        if response.function_calls:
            for function_call in response.function_calls:
                print(f"- Calling function: {function_call.name}")
                function_response_part = call_function(
                    function_call, verbose=args.verbose
                )
                function_responses.append(function_response_part)
                if args.verbose:
                    print(f"-> {function_response_part}")
                else:
                    print(f"-> {function_call.name}({function_call.args})")

            messages.append(
                types.Content(role="user", parts=function_responses)
            )
            continue

        final_response = response.text or ""
        print("Final response:")
        print(final_response)
        return

    print(
        "Error: reached the maximum number of iterations without receiving a final response."
    )
    sys.exit(1)


# def main():
#    print("Hello from personal-ai-agent!")


if __name__ == "__main__":
    main()
