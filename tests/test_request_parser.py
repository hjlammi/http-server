from server.request_parser import parse_request
import pytest

def test_parse_request_gets_GET_method_from_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1'
    request = parse_request(request_string)

    assert request.method == 'GET'

def test_parse_request_gets_uri_from_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1'
    request = parse_request(request_string)

    assert request.uri == '/path/to/example.com'

def test_parse_request_gets_http_version_from_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1'
    request = parse_request(request_string)

    assert request.http_version == 'HTTP/1.1'

def test_parse_request_sets_headers_to_None_when_there_are_no_headers_in_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1'
    request = parse_request(request_string)

    assert request.headers == None

def test_parse_request_parses_host_header_from_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org'
    request = parse_request(request_string)

    assert request.headers['host'] == 'www.w3.org'

def test_parse_request_parses_accept_header_from_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1\r\naccept: text/html'
    request = parse_request(request_string)

    assert request.headers['accept'] == 'text/html'

def test_parse_request_parses_two_headers_from_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\naccept: text/html'
    request = parse_request(request_string)

    assert len(request.headers) == 2

def test_parse_request_parses_accept_and_host_headers_from_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\naccept: text/html'
    request = parse_request(request_string)

    assert request.headers['accept'] == 'text/html'
    assert request.headers['host'] == 'www.w3.org'

def test_parse_request_parses_content_length_headers_from_the_request():
    request_string = 'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\naccept: text/html\r\ncontent-length: 4'
    request = parse_request(request_string)

    assert request.headers['content-length'] == '4'

def test_parses_request_message_from_browser_without_raising_error():
    request_string = 'GET / HTTP/1.1\r\nConnection: keep-alive\r\naccept: text/html,*/*\r\nuser-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36\r\nhost: 127.0.0.1:8000'
    request = parse_request(request_string)
