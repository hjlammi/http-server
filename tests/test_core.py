from server.core import *
import socket

HOST = "127.0.0.1"
PORT = 8000

def test_main_can_open_multiple_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock1:
        sock1.connect((HOST, PORT))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock2:
            sock2.settimeout(1)
            sock2.connect((HOST, PORT))
            sock2.sendall(b'GET /path/to/example.com HTTP/1.1\r\n\r\n')
            data = sock2.recv(1024)
