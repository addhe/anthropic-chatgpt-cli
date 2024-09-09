"""
Anthropic Bot: A simple chatbot using Anthropic's Claude API.

This script allows users to interact with Claude AI in a command-line
interface. It uses the Anthropic API to generate responses based on user input.

Author: [Your Name]
Date: [Current Date]
"""

import os
import time
from typing import List, Dict

import anthropic
from anthropic import Anthropic

# Constants
MODEL_NAME = "claude-3-sonnet-20240229"
MAX_TOKENS = 1024


def setup_anthropic_api() -> Anthropic:
    """Set up and return the Anthropic API client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Missing ANTHROPIC API Key.")
    return Anthropic(api_key=api_key)


def generate_response(
    client: Anthropic,
    prompt: str,
    conversation_history: List[Dict[str, str]]
) -> str:
    """Generate a response using the Anthropic API."""
    try:
        messages = conversation_history + [{"role": "user", "content": prompt}]
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            messages=messages
        )
        return response.content[0].text
    except anthropic.APIError as e:
        print(f"An API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return ""


def print_char_by_char(text: str) -> None:
    """Print text character by character with a slight delay."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()


def main() -> None:
    """Main function to run the Anthropic bot."""
    welcome_message = f"""
    Welcome to Anthropic Bot (Claude AI)!
    Using {MODEL_NAME} Text Generator made by (Awan),
    Happy chat and talk with your {MODEL_NAME} AI Generative Model
    Addhe Warman Putra - (Awan)

    Type 'exit()' to end the conversation.
    """
    print(welcome_message)

    client = setup_anthropic_api()
    conversation_history: List[Dict[str, str]] = []

    while True:
        user_input = input("\n> ").strip()
        if user_input.lower() == 'exit()':
            print("Thank you for using Anthropic Bot. Goodbye!")
            break

        response = generate_response(client, user_input, conversation_history)
        if response:
            print("\nClaude:", end=' ')
            print_char_by_char(response)
            conversation_history.extend([
                {"role": "human", "content": user_input},
                {"role": "assistant", "content": response}
            ])


if __name__ == "__main__":
    main()
