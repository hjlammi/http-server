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

    assert result == '<h1>/</h1><table><tbody><tr><td><a href="cat_pics">cat_pics/</a></td></tr><tr><td><a href="random">random/</a></td></tr><tr><td><a href="lorem_ipsum.txt">lorem_ipsum.txt</a></td></tr></tbody></table>'

def test_list_subdir_contents_in_html():
    result = list_dir_contents_in_html('tests/webroot/cat_pics', 'tests/webroot/')

    assert result == '<h1>/cat_pics</h1><table><tbody><tr><td><a href="2janu.jpg">2janu.jpg</a></td></tr><tr><td><a href="ella.jpg">ella.jpg</a></td></tr><tr><td><a href="janu.jpg">janu.jpg</a></td></tr></tbody></table>'

def test_read_text_file_contents():
    result = read_file_contents('tests/webroot/lorem_ipsum.txt')

    assert result == 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu.\n'

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

def test_get_relative_path_for_cat_pics_subdir_without_end_slash():
    assert get_relative_path('tests/webroot/cat_pics', 'tests/webroot') == '/cat_pics'
