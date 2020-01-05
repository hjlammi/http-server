from server.connection import Connection
import socket

HOST = "127.0.0.1"
PORT = 8800
ADDR = f'http://{HOST}:{PORT}'

def test_connection_sends_request():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
    lsock.bind((HOST, PORT))
    lsock.listen()
    lsock.setblocking(False)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    conn_sock, addr = lsock.accept()
    print('accepted connection from', addr)

    connection = Connection(ADDR, conn_sock)
    req_to_send = b'test'
    connection.send(req_to_send)
    connection.socket.close()

    req_to_receive = sock.recv(1024)
    assert req_to_receive == req_to_send
