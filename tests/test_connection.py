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

def test_send_changes_connection_state_as_sending_response():
    connection = Connection(ADDR, fake_socket)
    response = b'test'
    connection.send(response)

    assert connection.state == Connection.SENDING_RESPONSE

def test_cannot_send_after_connection_is_closed():
    connection = Connection(ADDR, fake_socket)
    connection.close()
    with pytest.raises(Exception, match='Connection closed'):
        connection.send(b'test')

def test_update_sends_whole_response_to_client():
    connection = Connection(ADDR, fake_socket)
    response = b'test'
    connection.send(response)
    connection.update()

    assert fake_socket.recv_buffer == response

def test_update_empties_send_buffer_after_sending_whole_response():
    connection = Connection(ADDR, fake_socket)
    response = b'test'
    connection.send(response)
    connection.update()

    assert not connection.send_buffer

def test_update_removes_beginning_of_response_from_send_buffer_with_longer_response():
    connection = Connection(ADDR, fake_socket)
    response = b'test longer response'
    connection.send(response)
    connection.update()

    assert connection.send_buffer == b' longer response' 
    assert fake_socket.recv_buffer == b'test' 

def test_update_called_twice_sends_the_whole_response():
    connection = Connection(ADDR, fake_socket)
    response = b'testing'
    connection.send(response)
    connection.update()
    connection.update()

    assert connection.send_buffer == b'' 
    assert fake_socket.recv_buffer == b'testing' 
