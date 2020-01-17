from server.connection import Connection
from fake_socket import FakeSocket
import pytest
from unittest.mock import Mock

HOST = "127.0.0.1"
PORT = 8800
ADDR = f'http://{HOST}:{PORT}'
BUFFER_SIZE = 4

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

def test_cannot_send_after_connection_is_closed():
    connection = Connection(ADDR, fake_socket)
    connection.close()
    with pytest.raises(Exception, match='Connection closed'):
        connection.send(b'')

def test_connection_stores_buffer_size_when_starting_to_receive_request():
    connection = Connection(ADDR, fake_socket)
    connection.receive(Mock(), BUFFER_SIZE)

    assert connection.buffer_size == BUFFER_SIZE

def test_connection_stores_callback_when_starting_to_receive_request():
    connection = Connection(ADDR, fake_socket)
    fake_callback = Mock()
    connection.receive(fake_callback, BUFFER_SIZE)

    assert connection.request_received_callback == fake_callback

def test_connection_changes_state_to_receiving_request_when_receive_called():
    connection = Connection(ADDR, fake_socket)
    connection.receive(Mock(), BUFFER_SIZE)

    assert connection.state == Connection.RECEIVING_REQUEST

def test_stores_received_request_in_recv_buffer():
    connection = Connection(ADDR, fake_socket)
    connection.receive(Mock(), BUFFER_SIZE)
    request = fake_socket.send_buffer
    connection.update()

    assert connection.recv_buffer == request

def test_connection_receives_first_4_bytes_of_longer_request():
    connection = Connection(ADDR, fake_socket)
    connection.receive(Mock(), BUFFER_SIZE)
    fake_socket.send_buffer = b'longer test request'
    connection.update()

    assert connection.recv_buffer == b'long'

def test_connection_receives_longer_request_in_two_chunks():
    connection = Connection(ADDR, fake_socket)
    connection.receive(Mock(), BUFFER_SIZE)
    fake_socket.send_buffer = b'longer test request'
    connection.update()
    connection.update()

    assert connection.recv_buffer == b'longer t'

def test_connection_changes_state_to_sending_after_receiving_the_whole_request():
    connection = Connection(ADDR, fake_socket)
    connection.receive(Mock(), BUFFER_SIZE)
    fake_socket.send_buffer = b'\r\n\r\n'
    connection.update()

    assert connection.state == Connection.SENDING_RESPONSE
