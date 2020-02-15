from server.request_parser import parse_request
import pytest

def test_parse_request_gets_GET_method_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\n'
    result = parse_request(request_line)

    assert result.method == 'GET'

def test_parse_request_gets_uri_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\n'
    result = parse_request(request_line)

    assert result.uri == '/path/to/example.com'

def test_parse_request_gets_http_version_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\n'
    result = parse_request(request_line)

    assert result.http_version == 'HTTP/1.1'

def test_parse_request_parses_host_header_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\n'
    result = parse_request(request_line)

    assert result.headers['Host'] == 'www.w3.org'

def test_parse_request_parses_accept_header_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\naccept: text/html\r\n'
    result = parse_request(request_line)

    assert result.headers['accept'] == 'text/html'

def test_parse_request_parses_two_headers_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\nHost: www.w3.org\r\naccept: text/html\r\n'
    result = parse_request(request_line)

    assert result.headers['accept'] == 'text/html'
    assert result.headers['Host'] == 'www.w3.org'

# # RFC2616 4.1. Message Types
def test_parse_request_should_not_throw_if_empty_lines_before_startline():
    request_line = '\r\n\r\nGET /path/to/example.com HTTP/1.1\r\naccept: text/html\r\n'
    parse_request(request_line)
