import socket
import threading

from base import PORT, ENCODING, DISCONNECT_MESSAGE
from base import send_header_and_data, recv_header_and_data

SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)

clients = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, socket.SOCK_STREAM)

server_socket.bind(ADDR)


def handle_clients(addr: tuple) -> None:
    """Handle each client connected to the server

    Args:
        addr (tuple): address of client
    """
    print(f'New connection, [{addr[0]}:{addr[1]}] connected.')
    while True:
        message_from_client = recv_header_and_data(clients[addr]).decode(encoding=ENCODING)
        print(f'[{addr[0]}:{addr[1]}] > {message_from_client}')
        if message_from_client == DISCONNECT_MESSAGE:
            break
        send_header_and_data(clients[addr], 'message receive'.encode(encoding=ENCODING))
    print(f'[{addr[0]}:{addr[1]}] disconnected.')


def start_server() -> None:
    """Start the server and listen for clients connections
    """
    server_socket.listen()
    print(f'📡 Server start at [{SERVER_IP}:{PORT}] 📡')
    while True:
        try:
            client_socket, client_address = server_socket.accept()
        except KeyboardInterrupt:
            break
        else:
            clients[client_address] = client_socket
            thread = threading.Thread(target=handle_clients, args=(client_address,))
            thread.start()

    server_socket.close()
    print('👻 Server down.')


if __name__ == '__main__':
    start_server()
