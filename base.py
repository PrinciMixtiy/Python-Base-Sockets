import socket
import threading
from tqdm import tqdm
import time


class BaseSocket:

    MAX_DATA_SIZE = 2048
    HEADER_LEN = 64
    PORT = 5050
    ENCODING = 'utf-8'

    def __init__(self):
        self.clientsocket: socket = None

    def recv_single_data(self, sock: socket, data_len: int, show_progress: bool = False):
        """Reveive data from another socket

        Args:
            sock (socket): socket reveiver
            data_len (int): data to be received length
            show_progress (bool, optional): show data reception progress. Defaults to False.

        Returns:
            bytes: data reveived
        """
        all_data = None
        len_bytes_reveived = 0

        if show_progress:
            progress = tqdm(range(data_len), f"Receiving data", unit="B", unit_scale=True,
                            unit_divisor=self.MAX_DATA_SIZE)

        while len_bytes_reveived < data_len:
            chunk_len = min(data_len - len_bytes_reveived, self.MAX_DATA_SIZE)
            data_part = sock.recv(chunk_len)

            if not data_part:
                return None
            if not all_data:
                all_data = data_part
            else:
                all_data += data_part

            len_bytes_reveived += len(data_part)

            if show_progress:
                progress.update(len(data_part))

        return all_data

    def send_data(self, data):
        """send data after his header to the receiver socket

        Args:
            data (bytes): data to send
        """
        data_header = str(len(data)).zfill(self.HEADER_LEN)
        self.clientsocket.sendall(data_header.encode(encoding=self.ENCODING))
        self.clientsocket.sendall(data)

    def recv_datas(self, sock: socket, show_progress: bool = False):
        """reveive data after his header from sender socket

        Args:
            sock (socket): socket reveiver
            show_progress (bool, optional): show data reception progress. Defaults to False.

        Returns:
            bytes: data received after sending data
        """
        header = self.recv_single_data(sock, self.HEADER_LEN)
        header = int(header.decode(encoding=self.ENCODING))
        data = self.recv_single_data(sock, header, show_progress)
        return data


class ClientSocket(BaseSocket):

    TIME_DELAY = 5

    def __init__(self):
        super().__init__()
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveraddress = (None, None)

    def close_socket(self):
        self.clientsocket.close()

    def connect(self, address: str):
        port: int = super().PORT
        i = 1
        while True:
            print(f'📡 Connexion au serveur {address}:{port} 📡')
            try:
                self.clientsocket.connect((address, port))
            except ConnectionRefusedError:
                print('❌ Erreur de connexion! ❌')
                i += 1
                print(f'🔁 Nouvelle tentative ( {i} ) 🔁')
                time.sleep(self.TIME_DELAY)
            else:
                print('\n✅ Connexion etablie avec succes ✅\n')
                self.serveraddress = address, port
                break


class ServerSocket(BaseSocket):

    IP = socket.gethostbyname(socket.gethostname())

    def __init__(self, ip: str = IP):
        super().__init__()
        self.sock: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, socket.SOCK_STREAM)
        self.sock.bind((ip, super().PORT))
        self.clientaddress = (None, None)

    def close_socket(self):
        self.sock.close()

    def listen(self):
        self.sock.listen()
        print(f'📡 Attente de connexion sur {self.IP}:{self.PORT} 📡')
        self.clientsocket, self.clientaddress = self.sock.accept()
        print(f'✅ Connectee avec {self.clientaddress[0]}:{self.clientaddress[1]} ✅\n')


class MultipleClientsServerSocket(ServerSocket):

    def __init__(self):
        super().__init__()
        self.clientsockets: dict = {}

    def handle_clients(self, addr: tuple):
        """Handle all client from listen_multiple_clients methode"""
        print(f'💻 {addr} connected 💻')
        print(f'💻 Client(s) connected: {threading.active_count()} 💻')

        connected = True
        while connected:
            client_message = self.recv_datas(self.clientsockets[addr]).decode(self.ENCODING)
            print(f'{addr} {client_message}')
            if client_message == 'exit':
                break

        self.clientsockets[addr].close()
        del self.clientsockets[addr]

    def linsten_multiple_clients(self):
        self.sock.listen()
        print(f'📡 Attente de connexion sur {self.IP}:{self.PORT} 📡')
        while True:
            clientsocket, clientaddress = self.sock.accept()
            self.clientsockets[clientaddress] = clientsocket
            thread = threading.Thread(target=self.handle_clients(clientaddress))
            thread.start()
