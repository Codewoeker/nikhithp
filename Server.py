import socket
import threading
import json
from googletrans import Translator

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
ACTIVE_CLIENTS = {}  # Dictionary to store (username, client) pairs with preferred language
BUFFER_SIZE = 2048

def listen_for_messages(client, username, translator):
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode('utf-8')

            if message:
                handle_client_message(client, username, message, translator)
            else:
                handle_client_disconnect(username)
                break
        except ConnectionResetError:
            handle_client_disconnect(username)
            break

def handle_client_message(client, username, message, translator):
    sender_language, country_location, content = message.split("::", 2)
    sender_language = sender_language.strip()

    # Translate message to English for broadcasting
    translated_message = translator.translate(content, dest='en').text
    final_msg = f"{username} ({sender_language}, {country_location}) -> {translated_message}"

    # Send the translated message to all clients
    send_msg_to_all(final_msg)

def send_msg_to_client(client, message):
    try:
        client.sendall(message.encode())
    except (socket.error, ConnectionResetError):
        pass  # Handle the case where the client has disconnected unexpectedly

def send_msg_to_all(message):
    for user, (client, _) in ACTIVE_CLIENTS.items():
        send_msg_to_client(client, message)

def handle_client_disconnect(username):
    if username in ACTIVE_CLIENTS:
        client, _ = ACTIVE_CLIENTS.pop(username)
        client.close()
        notify_clients(f"SERVER-> {username} has left the chat")

def notify_clients(message):
    send_msg_to_all(message)

def client_handler(client, address):
    try:
        # Receive username and preferred language from the client
        username = client.recv(BUFFER_SIZE).decode('utf-8')
        preferred_language = client.recv(BUFFER_SIZE).decode('utf-8')

        # Add the client to the ACTIVE_CLIENTS dictionary
        ACTIVE_CLIENTS[username] = (client, preferred_language)

        # Notify other clients about the new user
        join_message = f"SERVER-> {username} ({preferred_language}) added to the chat"
        notify_clients(join_message)

        translator = Translator()
        threading.Thread(target=listen_for_messages, args=(client, username, translator)).start()
    except (socket.error, ConnectionResetError):
        pass  # Handle the case where the client has disconnected unexpectedly

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")

    except socket.error as e:
        print(f"Unable to bind host and port: {e}")
        return

    server.listen(LISTENER_LIMIT)

    while True:
        try:
            client, address = server.accept()
            print(f"Successfully connected to client {address}")
            threading.Thread(target=client_handler, args=(client, address)).start()
        except socket.error as e:
            print(f"Error accepting client connection: {e}")

if __name__ == '__main__':
    main()
