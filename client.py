import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            # Receive and print messages from the server
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            print("Connection to the server has been lost.")
            break


def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    name_prompt = client_socket.recv(1024).decode('utf-8')
    print(name_prompt, end='')

    name = input()
    client_socket.send(f"{name}: joined the chat".encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        client_socket.send(f"{name}: {message}".encode('utf-8'))


if __name__ == "__main__":
    main()
