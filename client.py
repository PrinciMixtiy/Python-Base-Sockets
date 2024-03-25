import socket
import time

from base import PORT, DISCONNECT_MESSAGE, ENCODING
from base import recv_header_and_data, send_header_and_data

RETRY_CONNECT_DELAY = 2

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect(ip: str) -> None:
    """Connect to a server

    Args:
        ip (str): Server ip address
    """
    retry_count = 1
    while True:
        print(f'📡 Connect to server [{ip}:{PORT}] 📡')
        try:
            client_socket.connect((ip, PORT))
        except ConnectionRefusedError:
            print(f'❌ Connection error ❌')
            retry_count += 1
            print(f'🔁 Retry to connect [{retry_count} retry] 🔁')
            time.sleep(RETRY_CONNECT_DELAY)
        else:
            print('✅ Connected with server ✅')
            break


def run():
    while True:
        message = input('Your message: ')
        send_header_and_data(client_socket, message.encode(encoding=ENCODING))
        if message == DISCONNECT_MESSAGE:
            break
        response = recv_header_and_data(client_socket).decode(encoding=ENCODING)
        print(response)
    client_socket.close()


if __name__ == '__main__':
    server_ip = input('💻 Server IP: ')
    connect(server_ip)
    run()
