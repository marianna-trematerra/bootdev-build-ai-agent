import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("No API key found.")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = OpenAI(
	base_url="https://openrouter.ai/api/v1",
	api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    temperature=0
)

if response.usage is None:
        raise RuntimeError("No usage property.")

prompt_tokens = response.usage.prompt_tokens
completion_tokens = response.usage.completion_tokens

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")

print(f"Response: {response.choices[0].message.content}")

