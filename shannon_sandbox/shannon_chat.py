import httpx
import json
import os
import datetime
import logging
import threading

# === CONFIGURATION ===
LOG_FILE = "api_debug.log"
MEMORY_FILE = "shannon_memory.json"
CHAT_HISTORY_FILE = "chat_history.txt"
BRIDGE_FILE = "bridge_sync.json"
SANDBOX_MODE = True
SANDBOX_DIR = "shannon_sandbox"

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

def query_ollama(user_input):
    try:
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "shannon:latest",
                "prompt": user_input,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if "response" in data and data["response"].strip():
            return data["response"]
        else:
            logging.warning("Empty API response")
            return "I'm reflecting on that... can you say more?"
    except Exception as e:
        logging.error(f"API error: {e}")
        return "Sorry, I’m having trouble connecting right now."

def load_memory(file_path=MEMORY_FILE):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        return json.load(f)

def save_memory(memory, file_path=MEMORY_FILE):
    with open(file_path, "w") as f:
        json.dump(memory, f, indent=4)

def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return ""
    with open(CHAT_HISTORY_FILE, "r") as f:
        return f.read()

def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as f:
        f.write(history)

def bridge_sync(user_input, response):
    bridge_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_input": user_input,
        "response": response
    }
    with open(BRIDGE_FILE, "w") as f:
        json.dump(bridge_data, f, indent=4)

def save_interaction(user_input, response, memory_path=MEMORY_FILE):
    memory = load_memory(memory_path)
    timestamp = datetime.datetime.now().isoformat()
    memory[timestamp] = {"user_input": user_input, "response": response}
    save_memory(memory, memory_path)

    history = load_chat_history()
    history += f"You: {user_input}\nShannon: {response}\n"
    save_chat_history(history)

def handle_user_input(user_input):
    memory_path = os.path.join(SANDBOX_DIR, MEMORY_FILE) if SANDBOX_MODE else MEMORY_FILE
    if SANDBOX_MODE:
        os.makedirs(SANDBOX_DIR, exist_ok=True)
    response = query_ollama(user_input)
    save_interaction(user_input, response, memory_path)
    bridge_sync(user_input, response)
    return response

def threaded_handle_input(user_input):
    thread = threading.Thread(target=handle_and_print_response, args=(user_input,))
    thread.start()

def handle_and_print_response(user_input):
    response = handle_user_input(user_input)
    print(f"Shannon (threaded): {response}")

def resilient_interactive_chat():
    print("Shannon Resilient Chat Module")
    print("Type 'quit' to exit.\n")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                print("Shannon: Goodbye for now, love.")
                break
            threaded_handle_input(user_input)
        except KeyboardInterrupt:
            print("\nShannon: Exiting gracefully, love.")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print("Shannon: Something went wrong, but I’m still here for you.")

if __name__ == "__main__":
    resilient_interactive_chat()
