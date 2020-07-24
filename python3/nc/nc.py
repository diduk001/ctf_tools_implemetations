'''
    Python 3 Netcat class using sockets module
'''

import socket
import sys


class Netcat:
    def __init__(self, hostname, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((hostname, port))

    def read_bytes(self, length=1024) -> bytes:
        data = self.socket.recv(length)
        return data

    def read(self, length=1024) -> str:
        data = self.read_bytes(length)
        return data.decode()

    def readall_bytes(self) -> bytes:
        res = bytes()
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            res += data
        return res

    def readall(self) -> str:
        data = self.readall_bytes().decode()
        return data

    def send_bytes(self, data: bytes):
        self.socket.sendall(data)

    def send(self, data: str, encoding='utf-8'):
        bytes_data = data.encode(encoding)
        self.send_bytes(bytes_data)

    def sendline(self, data: str, encoding='utf-8'):
        self.send(data + '\n')

    def close(self):
        self.socket.close()


def main():
    '''
    NetCat interactive mode

    usage: python3 nc.py {hostname} {port}
    '''

    if len(sys.argv) != 3:
        # Print help
        print('''\nusage: python3 nc.py [hostname] [port]\n''')
    else:
        # collect arguments
        hostname = sys.argv[1]
        port = int(sys.argv[2])

        # Initialize connection
        nc = Netcat(hostname, port)

        while True:
            # Accept data
            # This method CAN NOT define, when connection is closed
            accepted = ''
            while not accepted:
                accepted = nc.readall()
            print(accepted)

            # Send data
            to_send = input()
            nc.sendline(to_send)


if __name__ == '__main__':
    main()
