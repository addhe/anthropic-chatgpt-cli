"""Anthropic Bot: A simple chatbot using Anthropic's Claude API.

This script allows users to interact with Claude AI in a command-line
interface. It uses the Anthropic API to generate responses based on user input.

Author: Addhe Warman Putra (Awan)
Date: 2024-10-06
"""

import os
import time
from typing import List, Dict
from functools import lru_cache

import anthropic
from anthropic import Anthropic, APIError

# Constants (now configurable)
MODEL_NAME = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
CACHE_SIZE = int(os.getenv("CACHE_SIZE", "100"))
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))


def setup_anthropic_api() -> Anthropic:
    """Set up and return the Anthropic API client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing ANTHROPIC API Key. "
            "Please set the ANTHROPIC_API_KEY environment variable."
        )
    return Anthropic(api_key=api_key)


@lru_cache(maxsize=CACHE_SIZE)
def generate_cached_response(prompt: str, conversation_key: str) -> str:
    """Generate a cached response using the Anthropic API."""
    client = setup_anthropic_api()
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            messages=messages
        )
        return response.content[0].text
    except APIError as e:
        print(f"Anthropic API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return ""


def generate_response(
    prompt: str,
    conversation_history: List[Dict[str, str]]
) -> str:
    """Generate a response using the cached function."""
    # Create a unique key for the cache based on the last few messages
    conversation_key = str(conversation_history[-MAX_HISTORY_MESSAGES:])
    return generate_cached_response(prompt, conversation_key)


def print_char_by_char(text: str) -> None:
    """Print text character by character with a slight delay."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()


def get_welcome_message() -> str:
    """Return the welcome message for the chatbot."""
    return (
        f"Welcome to Anthropic Bot (Claude AI)!\n"
        f"Using {MODEL_NAME} Text Generator made by (Awan),\n"
        f"Happy chat and talk with your {MODEL_NAME} AI Generative Model\n"
        "Addhe Warman Putra - (Awan)\n\n"
        "Type 'exit()' to end the conversation."
    )


def main() -> None:
    """Main function to run the Anthropic bot."""
    print(get_welcome_message())

    conversation_history: List[Dict[str, str]] = []

    while True:
        user_input = input("\n> ").strip()
        if user_input.lower() == 'exit()':
            print("Thank you for using Anthropic Bot. Goodbye!")
            break

        response = generate_response(user_input, conversation_history)
        if response:
            print_char_by_char(response)
            conversation_history.extend([
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": response}
            ])

        # Trim conversation history to manage token usage
        conversation_history = conversation_history[-MAX_HISTORY_MESSAGES:]


if __name__ == "__main__":
    main()
