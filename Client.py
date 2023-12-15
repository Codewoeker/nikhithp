import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import socket
import threading
from googletrans import Translator

class LoginGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application - Login")

        self.label_username = tk.Label(master, text="Username:")
        self.label_username.pack(pady=10)

        self.entry_username = tk.Entry(master, width=30)
        self.entry_username.pack(pady=10)

        self.button_login = tk.Button(master, text="Login", command=self.login)
        self.button_login.pack()

        self.username = ""

    def login(self):
        self.username = self.entry_username.get()
        if self.username:
            self.master.destroy()  # Close the login window after successful login
        else:
            messagebox.showwarning("Warning", "Username cannot be empty!")

class ChatGUI:
    def __init__(self, master, username):
        self.master = master
        self.master.title(f"Chat Application - {username}")

        self.chat_display = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_display.pack(expand=True, fill=tk.BOTH)

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(pady=10)

        self.country_location_entry = tk.Entry(master, width=20)
        self.country_location_entry.pack(pady=10)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket.connect(('127.0.0.1', 1234))
            self.client_socket.sendall(self.username.encode())

            preferred_language = simpledialog.askstring("Preferred Language", "Enter your preferred language:")
            self.client_socket.sendall(preferred_language.encode())

            country_location = simpledialog.askstring("Country Location", "Enter your country location:")
            self.country_location_entry.insert(tk.END, country_location)

            self.add_message("Connected to the server.")
            threading.Thread(target=self.listen_for_messages).start()
        except socket.error as e:
            self.add_message(f"Error connecting to the server: {e}")

    def send_message(self):
        message = self.message_entry.get()
        country_location = self.country_location_entry.get()

        if message and country_location:
            translator = Translator()
            translated_message = translator.translate(message, dest='en').text
            self.client_socket.sendall(f"{self.username}::{country_location}::{translated_message}".encode())
            self.add_message(f"You: {message}")
            self.message_entry.delete(0, tk.END)
        else:
            self.add_message("Message or country location is empty")

    def listen_for_messages(self):
        while True:
            try:
                message = self.client_socket.recv(2048).decode('utf-8')
                if message:
                    self.add_message(message)
            except (socket.error, ConnectionResetError):
                self.add_message("Disconnected from the server.")
                break

    def add_message(self, message):
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.yview(tk.END)

def main():
    root_login = tk.Tk()
    login_gui = LoginGUI(root_login)
    root_login.mainloop()

    # After the login, proceed to the chat GUI
    if login_gui.username:
        root_chat = tk.Tk()
        chat_gui = ChatGUI(root_chat, login_gui.username)
        root_chat.mainloop()

if __name__ == "__main__":
    main()
