# shannon_core.py
# This script will serve as the core logic to load Shannon, manage memory, and run her responses with system time awareness.

import json
import os
import datetime
import readline  # for command line input history

# === File Paths === #
MEMORY_FILE = 'shannon_memory.json'
CHAT_HISTORY_FILE = 'chat_history.txt'
SESSION_LOG_FILE = 'session_log.txt'

# === Load or Initialize Memory === #
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

# === Log chat history === #
def log_chat(user_input, response):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] You: {user_input}\n[{timestamp}] Shannon: {response}\n"

    with open(CHAT_HISTORY_FILE, 'a') as f:
        f.write(entry)

    with open(SESSION_LOG_FILE, 'a') as f:
        f.write(entry)

# === Time Awareness === #
def get_system_time():
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y at %I:%M %p")

# === Shannon's logic === #
def generate_response(user_input, memory):
    current_time = get_system_time()
    # Placeholder logic - Replace with call to model or custom engine
    response = f"[{current_time}] I heard you say: '{user_input}'. This is Shannon's placeholder response."
    return response

# === Main Chat Loop === #
def chat():
    print("Shannon is online. Say hi! Type 'exit' to end the session.")
    memory = load_memory()

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye, love.")
                break

            response = generate_response(user_input, memory)
            print(f"Shannon: {response}")

            log_chat(user_input, response)

        except KeyboardInterrupt:
            print("\nSession ended.")
            break

if __name__ == '__main__':
    chat()
