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
    connection = Connection(ADDR, fake_socket, Mock())
    response = b'test'
    connection.send(response)

    assert connection.send_buffer == response

def test_send_changes_connection_state_as_sending_response():
    connection = Connection(ADDR, fake_socket, Mock())
    response = b'test'
    connection.send(response)

    assert connection.state == Connection.SENDING_RESPONSE

def test_cannot_send_after_connection_is_closed():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.close()
    with pytest.raises(Exception, match='Connection closed'):
        connection.send(b'test')

def test_update_sends_whole_response_to_client():
    connection = Connection(ADDR, fake_socket, Mock())
    response = b'test'
    connection.send(response)
    connection.update()

    assert fake_socket.recv_buffer == response

def test_update_empties_send_buffer_after_sending_whole_response():
    connection = Connection(ADDR, fake_socket, Mock())
    response = b'test'
    connection.send(response)
    connection.update()

    assert not connection.send_buffer

def test_update_removes_beginning_of_response_from_send_buffer_with_longer_response():
    connection = Connection(ADDR, fake_socket, Mock())
    response = b'test longer response'
    connection.send(response)
    connection.update()

    assert connection.send_buffer == b' longer response'
    assert fake_socket.recv_buffer == b'test'

def test_update_called_twice_sends_the_whole_response():
    connection = Connection(ADDR, fake_socket, Mock())
    response = b'testing'
    connection.send(response)
    connection.update()
    connection.update()

    assert connection.send_buffer == b''
    assert fake_socket.recv_buffer == b'testing'

def test_state_is_changed_to_closed_when_close_is_called():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.close()

    assert connection.state == Connection.CLOSED

def test_cannot_send_after_connection_is_closed():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.close()
    with pytest.raises(Exception, match='Connection closed'):
        connection.send(b'')

def test_connection_stores_buffer_size_when_starting_to_receive_request():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.receive(Mock(), BUFFER_SIZE)

    assert connection.buffer_size == BUFFER_SIZE

def test_connection_stores_callback_when_starting_to_receive_request():
    connection = Connection(ADDR, fake_socket, Mock())
    received_callback = Mock()
    connection.receive(received_callback, BUFFER_SIZE)

    assert connection.request_received_callback == received_callback

def test_connection_changes_state_to_receiving_request_when_receive_called():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.receive(Mock(), BUFFER_SIZE)

    assert connection.state == Connection.RECEIVING_REQUEST

def test_stores_received_request_in_recv_buffer():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.receive(Mock(), BUFFER_SIZE)
    request = fake_socket.send_buffer
    connection.update()

    assert connection.recv_buffer == request

def test_connection_receives_first_4_bytes_of_longer_request():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.receive(Mock(), BUFFER_SIZE)
    fake_socket.send_buffer = b'longer test request'
    connection.update()

    assert connection.recv_buffer == b'long'

def test_connection_receives_longer_request_in_two_chunks():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.receive(Mock(), BUFFER_SIZE)
    fake_socket.send_buffer = b'longer test request'
    connection.update()
    connection.update()

    assert connection.recv_buffer == b'longer t'

def test_connection_is_closed_if_nothing_received_from_the_client():
    close_callback = Mock()
    connection = Connection(ADDR, fake_socket, close_callback)
    connection.receive(Mock(), BUFFER_SIZE)
    fake_socket.send_buffer = b''
    connection.update()

    close_callback.assert_called_with(connection.socket)

def test_received_callback_is_called_with_connection_as_parameter_after_whole_request_is_received():
    connection = Connection(ADDR, fake_socket, Mock())
    received_callback = Mock()
    connection.receive(received_callback, 70)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\n\r\n'
    connection.update()

    received_callback.assert_called_with(connection)

def test_connection_is_closed_after_the_whole_response_is_sent():
    close_callback = Mock()
    connection = Connection(ADDR, fake_socket, close_callback)
    response = b'test'
    connection.send(response)
    connection.update()

    close_callback.assert_called_with(connection.socket)

def test_connection_updates_raises_error_if_socket_does_not_send_anything():
    connection = Connection(ADDR, fake_socket, Mock())
    connection.send_buffer = b''
    connection.state = Connection.SENDING_RESPONSE

    with pytest.raises(Exception, match='Socket connection broken'):
        connection.update()

def test_parsed_request_is_stored_in_the_connection():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 100
    connection.receive(Mock(), buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\naccept: text/html\r\n\r\n'
    connection.update()

    assert connection.parsed_request.method == 'GET'
    assert connection.parsed_request.uri == '/path/to/example.com'
    assert connection.parsed_request.http_version == 'HTTP/1.1'
    assert connection.parsed_request.headers == {'Host': 'www.w3.org', 'accept': 'text/html'}

def test_no_request_body_read_without_content_length_header():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 78
    connection.receive(Mock(), buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\naccept: text/html\r\n\r\ntest'
    connection.update()

    assert connection.request_body == None

def test_short_request_body_is_stored_in_the_connection():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 100
    connection.receive(Mock(), buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\naccept: text/html\r\ncontent-length: 4\r\n\r\ntest'
    connection.update()

    assert connection.request_body == b'test'

def test_body_is_read_only_the_amount_of_content_length():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 100
    connection.receive(Mock(), buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\naccept: text/html\r\ncontent-length: 3\r\n\r\ntest'
    connection.update()

    assert connection.request_body == b'tes'

def test_request_received_callback_called_after_startline_and_headers_read_but_body_is_not():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 56
    received_callback = Mock()
    connection.receive(received_callback, buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\ncontent-length: 4\r\n\r\ntest'
    connection.update()

    assert connection.state == Connection.RECEIVING_BODY

def test_update_reads_request_body_after_headers_received():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 56
    received_callback = Mock()
    connection.receive(received_callback, buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\ncontent-length: 4\r\n\r\ntest'
    connection.update()
    connection.update()

    assert connection.request_body == b'test'

def test_update_reads_longer_request_body_after_headers_received():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 56
    received_callback = Mock()
    connection.receive(received_callback, buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\ncontent-length: 105\r\n\r\nthis is a very long request body that will be read in two parts because it is longer than the buffer size'
    connection.update()
    connection.update()
    connection.update()

    assert connection.request_body == b'this is a very long request body that will be read in two parts because it is longer than the buffer size'

def test_part_of_the_body_read_when_headers_and_rest_with_another_update_call():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 57
    received_callback = Mock()
    connection.receive(received_callback, buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\ncontent-length: 4\r\n\r\ntest'
    connection.update()
    assert connection.request_body == b't'

    connection.update()
    assert connection.request_body == b'test'

def test_body_is_not_read_as_a_whole_because_content_length_is_shorter():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 57
    received_callback = Mock()
    connection.receive(received_callback, buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\ncontent-length: 4\r\n\r\ntesting a bit longer body that is not read in its entirety'
    connection.update()
    connection.update()
    assert connection.request_body == b'test'

def test_body_is_not_read_as_a_whole_because_content_length_is_shorter_for_longer_message():
    connection = Connection(ADDR, fake_socket, Mock())
    buffer_size = 58
    received_callback = Mock()
    connection.receive(received_callback, buffer_size)
    fake_socket.send_buffer = b'GET /path/to/example.com HTTP/1.1\r\ncontent-length: 60\r\n\r\ntesting a somewhat longer body that is not read in its entirety'
    connection.update()
    assert connection.request_body == b't'

    connection.update()
    assert connection.request_body == b'testing a somewhat longer body that is not read in its enti'

    connection.update()
    assert connection.request_body == b'testing a somewhat longer body that is not read in its entir'
