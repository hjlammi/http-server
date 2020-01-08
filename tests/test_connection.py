from server.connection import Connection
from fake_socket import FakeSocket
import pytest

HOST = "127.0.0.1"
PORT = 8800
ADDR = f'http://{HOST}:{PORT}'

def setup_function():
    global fake_socket
    fake_socket = FakeSocket()

def test_send_stores_response_to_send_buffer():
    connection = Connection(ADDR, fake_socket)
    response = b'test'
    connection.send(response)

    assert connection.send_buffer == response

def test_cannot_send_after_connection_is_closed():
    connection = Connection(ADDR, fake_socket)
    connection.close()
    with pytest.raises(Exception, match='Connection closed'):
        connection.send(b'test')

def test_connection_writes_part_of_longer_response_in_send_buffer():
    connection = Connection(ADDR, fake_socket)
    response = b'This is a longer test response'
    len_res_sent = connection.send(response)

    assert fake_socket.send_buffer == response[:len_res_sent]

def test_part_that_was_already_sent_gets_removed_from_response():
    connection = Connection(ADDR, fake_socket)
    response = b'This is a longer test response'
    connection.send(response)

    assert connection.response_left == response[FakeSocket.BUFFER_SIZE:]
