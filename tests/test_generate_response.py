from server.request import Request
from server.generate_response import *
import pytest

def test_generate_response_for_HEAD_request():
    request = Request('HEAD', '/', None, None, None)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 213\r\n\r\n'
    assert generate_response(request, 'tests/webroot') == expected_result

def test_generate_response_for_GET_request():
    request = Request('GET', '/', None, None, None)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 213\r\n\r\n<h1>tests/webroot</h1><table><tbody><tr><td><a href="cat_pics">cat_pics/</a></td></tr><tr><td><a href="random">random/</a></td></tr><tr><td><a href="lorem_ipsum.txt">lorem_ipsum.txt</a></td></tr></tbody></table>\r\n'
    assert generate_response(request, 'tests/webroot') == expected_result

def test_get_contents_from_root():
    result = get_contents_from_dir('tests/webroot')

    assert result == ['cat_pics/', 'random/', 'lorem_ipsum.txt']

@pytest.mark.focus
def test_get_contents_from_subdir():
    result = get_contents_from_dir('tests/webroot/cat_pics')

    assert result == ['2janu.jpg', 'ella.jpg', 'janu.jpg']

def test_create_html_body():
    result = create_html_body('tests/webroot')

    assert result == '<h1>tests/webroot</h1><table><tbody><tr><td><a href="cat_pics">cat_pics/</a></td></tr><tr><td><a href="random">random/</a></td></tr><tr><td><a href="lorem_ipsum.txt">lorem_ipsum.txt</a></td></tr></tbody></table>'

def test_read_text_file_contents():
    result = read_file_contents('tests/webroot/lorem_ipsum.txt')

    assert result == 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu.\n'

def test_text_file_is_a_file():
    assert is_file('/lorem_ipsum.txt') == True

def test_dir_is_not_a_file():
    assert is_file('/cat_pics/') == False
