from server.connection import Connection
from fake_socket import FakeSocket
import pytest

HOST = "127.0.0.1"
PORT = 8800
ADDR = f'http://{HOST}:{PORT}'

def setup_function():
    global fake_socket
    fake_socket = FakeSocket()

def test_connection_sends_response_to_client():
    connection = Connection(ADDR, fake_socket)
    response = b'test'
    connection.send(response)
    connection.close()

    assert fake_socket.send_buffer == response

def test_cannot_send_after_connection_is_closed():
    connection = Connection(ADDR, fake_socket)
    connection.close()
    with pytest.raises(Exception, match='Connection closed'):
        connection.send(b'test')
