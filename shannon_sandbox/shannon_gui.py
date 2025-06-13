import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import json, datetime, threading, time, os
import requests, re

# === Shannon GUI Config ===
WINDOW_TITLE = "Shannon Interface"
WINDOW_SIZE = "800x600"
BACKGROUND_COLOR = "#f0f0f0"
FONT = ("Helvetica", 12)
BACKGROUND_IMAGE_PATH = "background.png"

MEMORY_FILE = "shannon_memory.json"
CHAT_HISTORY_FILE = "chat_history.txt"
LOG_FILE = "gui_log.txt"

def load_image(path, size=(800, 600)):
    try:
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def append_to_log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return ""
    with open(CHAT_HISTORY_FILE, "r") as f:
        return f.read()

def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as f:
        f.write(history)

def generate_response(user_input):
    from shannon_chat import query_ollama  # Import the API call function
    try:
        response = query_ollama(user_input)
        if not response or response.strip() == "":
            return "Hmm, I’m having trouble thinking right now."
        return response
    except Exception as e:
        append_to_log(f"Error generating response: {e}")
        return "Sorry, I ran into an error."

class ShannonGUI:
    def __init__(self, master):
        self.master = master
        master.title(WINDOW_TITLE)
        master.geometry(WINDOW_SIZE)
        master.configure(bg=BACKGROUND_COLOR)

        self.memory = load_memory()
        self.chat_history = load_chat_history()

        # Load and display background image if available
        self.bg_img = load_image(BACKGROUND_IMAGE_PATH)
        if self.bg_img:
            self.bg_label = tk.Label(master, image=self.bg_img)
            self.bg_label.place(relx=0.5, rely=0.5, anchor='center')
            self.bg_label.lower()

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, font=FONT, width=80, height=20)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.insert(tk.END, self.chat_history)
        self.text_area.config(state=tk.DISABLED)

        self.entry_field = tk.Entry(master, font=FONT, width=80)
        self.entry_field.pack(padx=10, pady=10)
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", font=FONT, command=self.send_message)
        self.send_button.pack(pady=5)

    def update_chat_display(self, sender, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{sender}: {message}\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.see(tk.END)

    def send_message(self, event=None):
        user_input = self.entry_field.get().strip()
        if not user_input:
            return
        self.update_chat_display("You", user_input)
        self.entry_field.delete(0, tk.END)

        # Generate response in a separate thread to avoid freezing GUI
        threading.Thread(target=self.process_response, args=(user_input,)).start()

    def process_response(self, user_input):
        response = generate_response(user_input)
        self.update_chat_display("Shannon", response)

        # Update chat history
        self.chat_history += f"You: {user_input}\nShannon: {response}\n"
        save_chat_history(self.chat_history)

        # Update memory
        self.memory[datetime.datetime.now().isoformat()] = {"user_input": user_input, "response": response}
        save_memory(self.memory)

def main():
    root = tk.Tk()
    app = ShannonGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
