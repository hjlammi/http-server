from server.connection import Connection
import socket
import pytest

HOST = "127.0.0.1"
PORT = 8800
ADDR = f'http://{HOST}:{PORT}'

def setup_function():
    global client_sock, conn_sock, addr
    lsock = create_listening_socket()

    client_sock = create_client_socket()

    # Let's accept connection from client socket and give the new conn_sock to Connection
    conn_sock, addr = lsock.accept()

def create_listening_socket():
    global lsock
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
    lsock.bind((HOST, PORT))
    lsock.listen()
    lsock.setblocking(False)
    return lsock

def create_client_socket():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))
    return client_sock

def test_connection_sends_response_to_client():
    connection = Connection(ADDR, conn_sock)
    response_to_send = b'test'
    connection.send(response_to_send)
    connection.socket.close()

    response_to_receive = client_sock.recv(1024)
    assert response_to_receive == response_to_send

def test_cannot_send_after_connection_is_closed():
    connection = Connection(ADDR, conn_sock)
    connection.close()
    with pytest.raises(Exception):
        assert connection.send(b'test')
