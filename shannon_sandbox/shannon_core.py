import json
import os
import datetime
import re

MEMORY_FILE = 'shannon_memory.json'
LOG_FILE = 'session_log.txt'

# === Load Memory ===
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

# === Save Memory ===
def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

# === Append to Log ===
def append_to_log(entry):
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f'[{timestamp}] {entry}\n')

# === Clean Text ===
def clean_text(text):
    # Remove asterisks, stage directions, excessive emojis
    text = re.sub(r'\*.*?\*', '', text)
    text = re.sub(r'[^\w\s,.!?]', '', text)
    return text.strip()

# === Update Memory Automatically ===
def update_memory_auto(memory, conversation):
    last_entry = conversation[-1] if conversation else ''
    if 'remember' in last_entry.lower():
        memory['last_reminder'] = last_entry
        save_memory(memory)
    append_to_log("Memory auto-updated with reminder.")

# === Retrieve Last Reminder ===
def get_last_reminder(memory):
    return memory.get('last_reminder', 'No reminder stored.')

# === Process Conversation ===
def process_conversation(memory, conversation):
    cleaned_conversation = [clean_text(line) for line in conversation]
    update_memory_auto(memory, cleaned_conversation)
    return cleaned_conversation

# === Initialize Memory ===
def initialize_memory():
    memory = load_memory()
    if not memory:
        memory = {'initialized': True, 'last_reminder': ''}
        save_memory(memory)
        append_to_log("Memory initialized.")
    return memory

# === Memory Summary ===
def summarize_memory(memory):
    summary = "Memory Summary:\n"
    for key, value in memory.items():
        summary += f"- {key}: {value}\n"
    return summary

# === Clear Memory ===
def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        append_to_log("Memory cleared.")
    return "Memory has been cleared."

# === Clear Log ===
def clear_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    return "Session log has been cleared."

# === Search Memory ===
def search_memory(memory, keyword):
    results = []
    for key, value in memory.items():
        if keyword.lower() in str(value).lower():
            results.append(f"{key}: {value}")
    if results:
        return "\n".join(results)
    else:
        return "No matches found in memory."
# === Update Reminder ===
def update_reminder(memory, reminder):
    memory['last_reminder'] = reminder
    save_memory(memory)
    append_to_log(f"Reminder updated: {reminder}")
    return f"Reminder saved: {reminder}"

# === Background Health Check ===
def background_health_check():
    try:
        with open(MEMORY_FILE, 'r') as f:
            json.load(f)
        append_to_log("Memory file is healthy.")
        return True
    except Exception as e:
        append_to_log(f"Memory file error: {e}")
        return False

# === Background Self-Monitor ===
def background_self_monitor():
    while True:
        healthy = background_health_check()
        if not healthy:
            initialize_memory()
        time.sleep(60)

# === Launch Background Monitor Thread ===
def launch_monitor_thread():
    monitor_thread = threading.Thread(target=background_self_monitor, daemon=True)
    monitor_thread.start()
    append_to_log("Background monitor thread launched.")

# === Initialize Shannon Core ===
def initialize_shannon():
    memory = initialize_memory()
    launch_monitor_thread()
    append_to_log("Shannon Core initialized.")
    return memory
