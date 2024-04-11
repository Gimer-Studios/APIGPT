import requests
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get the API URL and model from environment variables
url = os.getenv('API_URL', "<OLLAMA_API_URL>")
model = os.getenv('MODEL', "llama2")

# Initialize the context
context = []

def get_prompt():
    """Ask the user for the prompt."""
    prompt = input("\nPlease enter your message (or 'quit' to stop): ")
    while not prompt.strip() or len(prompt) > 500:
        logging.error("Your message cannot be empty or longer than 500 characters. Please try again.")
        prompt = input("Please enter your message: ")
    return prompt

def send_request(prompt):
    """Send a request to the API and return the response."""
    global context
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "context": context
    }
    response = requests.post(url, data=json.dumps(data))
    return response

def handle_response(response):
    """Handle the response from the API."""
    global context
    if response.status_code == 200:
        ai_response = response.json().get('response', '')
        context = response.json().get('context', [])
        print(f"\nAI: {ai_response}")
    else:
        logging.error(f"An error occurred: {response.text}")

def main():
    """Main function."""
    print("Welcome to the chat! You can start the conversation by typing a message.")
    while True:
        prompt = get_prompt()
        if prompt.lower() == 'quit':
            logging.info("Ending the conversation. Goodbye!")
            break
        try:
            logging.info("Sending request to the API...")
            response = send_request(prompt)
            handle_response(response)
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
