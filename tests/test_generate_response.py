from server.request import Request
from server.generate_response import *
import pytest

def test_generate_response_for_HEAD_request():
    request = Request('HEAD', '/', None, None, None)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 201\r\n\r\n'
    assert generate_response(request, 'tests/webroot') == expected_result

def test_generate_response_for_GET_request():
    request = Request('GET', '/', None, None, None)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 201\r\n\r\n<h1>/</h1><table><tbody><tr><td><a href="cat_pics">cat_pics/</a></td></tr><tr><td><a href="random">random/</a></td></tr><tr><td><a href="lorem_ipsum.txt">lorem_ipsum.txt</a></td></tr></tbody></table>\r\n'
    assert generate_response(request, 'tests/webroot') == expected_result

def test_get_contents_from_root():
    result = get_contents_from_dir('tests/webroot')

    assert result == ['cat_pics/', 'random/', 'lorem_ipsum.txt']

@pytest.mark.focus
def test_get_contents_from_subdir():
    result = get_contents_from_dir('tests/webroot/cat_pics')

    assert result == ['2janu.jpg', 'ella.jpg', 'janu.jpg']

def test_list_dir_contents_in_html():
    result = list_dir_contents_in_html('tests/webroot', 'tests/webroot')

    assert result == b'<h1>/</h1><table><tbody><tr><td><a href="cat_pics">cat_pics/</a></td></tr><tr><td><a href="random">random/</a></td></tr><tr><td><a href="lorem_ipsum.txt">lorem_ipsum.txt</a></td></tr></tbody></table>'

def test_list_subdir_contents_in_html():
    result = list_dir_contents_in_html('tests/webroot/cat_pics', 'tests/webroot/')

    assert result == b'<h1>/cat_pics</h1><table><tbody><tr><td><a href="2janu.jpg">2janu.jpg</a></td></tr><tr><td><a href="ella.jpg">ella.jpg</a></td></tr><tr><td><a href="janu.jpg">janu.jpg</a></td></tr></tbody></table>'

def test_read_text_file_contents_in_bytes():
    result = read_file_contents_in_bytes('tests/webroot/lorem_ipsum.txt')

    assert result == b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu.\n'

def test_is_a_valid_resource():
    assert is_a_valid_resource('tests/webroot/lorem_ipsum.txt') == True

def test_is_a_valid_directory():
    assert is_a_valid_resource('tests/webroot/cat_pics') == True

def test_is_not_a_valid_resource_as_it_does_not_exist():
    assert is_a_valid_resource('tests/webroot/cat_pics.txt') == False

def test_get_relative_path_for_root_dir():
    assert get_relative_path('tests/webroot/', 'tests/webroot/') == '/'

def test_get_relative_path_for_root_dir_without_end_slash():
    assert get_relative_path('tests/webroot', 'tests/webroot') == '/'

def test_get_relative_path_for_cat_pics_subdir():
    assert get_relative_path('tests/webroot/cat_pics', 'tests/webroot/') == '/cat_pics'

def test_sends_redirect_response_if_dir_without_end_slash():
    request = Request('GET', '/cat_pics', None, None, None)
    expected_result = b'HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nLocation: /cat_pics/\r\n\r\n'
    assert generate_response(request, 'tests/webroot') == expected_result

def test_generate_301_response():
    request = Request('GET', '/cat_pics', None, None, None)
    expected_response = b'HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nLocation: /cat_pics/\r\n\r\n'
    assert generate_301_response(request) == expected_response

def test_read_image_file_contents_in_bytes():
    expected = 'ffd8ffe1a3fe'
    assert read_file_contents_in_bytes('tests/webroot/cat_pics/ella.jpg')[:6].hex() == expected

def test_generate_response_with_png_mime_type_and_bytes_body():
    request = Request('GET', '/random/Screenshot_20161222-082602.png', None, None, None)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\nContent-Length: 62995\r\n\r\n\x89PN'
    assert generate_response(request, 'tests/webroot')[:70] == expected_result

def test_generate_404_response():
    request = Request('GET', '/notfound', None, None, None)
    expected_response = b'HTTP/1.1 404 Not Found\r\nContent-Length: 25\r\nLocation: /notfound/\r\n\r\n<h1>Page not found</h1>\r\n'
    assert generate_404_response(request) == expected_response

def test_generate_response_with_file_contents_for_text_file():
    path_to_resource = 'tests/webroot/lorem_ipsum.txt'
    mime_type = 'text/plain'
    expected_response = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 362\r\n\r\nLorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu.\n'
    assert generate_response_for_a_file_request(path_to_resource, mime_type) == expected_response

def test_generate_response_with_file_contents_for_image_file():
    path_to_resource = 'tests/webroot/cat_pics/ella.jpg'
    mime_type = 'image/jpeg'
    expected_beginning_of_response = b'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: 1033012\r\n\r\n\xff\xd8\xff\xe1\xa3\xfe'
    assert generate_response_for_a_file_request(path_to_resource, mime_type)[:76] == expected_beginning_of_response
