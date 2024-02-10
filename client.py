from base import ClientSocket

if __name__ == '__main__':
    client = ClientSocket()

    ip = input('IP: ')

    client.connect(ip)

    message = ''
    while message != 'exit':
        message = input('> ')
        client.send_data(message.encode(client.ENCODING))

    client.close_socket()
