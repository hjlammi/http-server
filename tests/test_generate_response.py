from server.request import Request
from server.generate_response import generate_response, get_contents_from_dir
import pytest

def test_generate_response_for_HEAD_request():
    request = Request('HEAD', '/', None, None, None)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 22\r\n\r\n'
    assert generate_response(request, None) == expected_result

def test_generate_response_for_GET_request():
    request = Request('GET', '/', None, None, None)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 22\r\n\r\n<h1>Hello World</h1>\r\n'
    assert generate_response(request, None) == expected_result

@pytest.mark.focus
def test_get_contents_from_root():
    result = get_contents_from_dir('tests/webroot')

    assert result == ['cat_pics/', 'random/', 'lorem_ipsum.text']

@pytest.mark.focus
def test_get_contents_from_subdir():
    result = get_contents_from_dir('tests/webroot/cat_pics')

    assert result == ['2janu.jpg', 'ella.jpg', 'janu.jpg']
