from server.request import Request
from server.generate_response import generate_response, get_contents_from_dir, create_html_body
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
