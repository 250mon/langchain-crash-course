from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json
import os

# Load environment variables
load_dotenv()

# Define the local file path for chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Function to load chat history from a local file
def load_chat_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

# Function to save chat history to a local file
def save_chat_history(file_path, chat_history):
    with open(file_path, "w") as file:
        json.dump(chat_history, file, indent=4)

# Load existing chat history
chat_history = load_chat_history(CHAT_HISTORY_FILE)
print("Chat History Loaded.")
print("Current Chat History:", chat_history)

# Initialize Chat Model
model = ChatOpenAI()

print("Start chatting with the AI. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # Send user input to the model and get the response
    response = model.invoke(user_input)
    print(f"AI: {response.content}")

    # Update chat history
    chat_history.append({"user": user_input, "ai": response.content})

    # Save updated chat history to the local file
    save_chat_history(CHAT_HISTORY_FILE, chat_history)