import socket
import threading

client_names = {}


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')

            message_parts = message.split(':', 1)

            if len(message_parts) == 2:
                name, msg = message_parts

                broadcast(name, msg)
            else:

                print(f"Received an invalid message: {message}")

        except ConnectionResetError:
            remove_client(client_socket)


def broadcast(name, message):
    # Send the message to all connected clients
    for client, client_name in client_names.items():
        try:
            client.send(f"{name}: {message}".encode('utf-8'))
        except:
            # Remove client name and close the connection on error
            remove_client(client)


def remove_client(client_socket):
    # Remove client name and close the connection
    if client_socket in client_names:
        name = client_names[client_socket]
        print(f"{name} has left the chat.")
        del client_names[client_socket]
    client_socket.close()


def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:

        client_socket, addr = server_socket.accept()
        print(f"Connection established from {addr}")

        client_socket.send("Enter your name: ".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8')

        client_names[client_socket] = name

        broadcast("Server", f"{name} has joined the chat.")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()
