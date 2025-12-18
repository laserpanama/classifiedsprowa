import os
from dotenv import load_dotenv

# It's good practice to load .env file at the start of the service
# that needs it.
load_dotenv(dotenv_path="app/backend/.env")

# This service will be responsible for interacting with the LLM
# to generate ad text.

# from emergentintegrations.llm.chat import LlmChat, UserMessage

def generate_ad_text(prompt: str) -> str:
    """
    Generates ad text based on a prompt.
    Checks for the UNIVERSAL_KEY in environment variables.
    """
    universal_key = os.getenv("UNIVERSAL_KEY")

    if not universal_key or universal_key == "dummy_key_replace_me":
        return "Warning: UNIVERSAL_KEY is not configured. Please set it in the .env file. Using placeholder text."

    # In a real implementation, this would call the LLM.
    # For now, it returns a placeholder string that indicates a valid key is present.

    # llm = LlmChat(api_key=universal_key)
    # response = llm.get_response([UserMessage(prompt)])
    # return response

    return f"This is a generated ad for the prompt: '{prompt}' (simulating a valid API key)"
