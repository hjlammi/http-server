from server.request_parser import parse_request
import pytest

def test_parse_request_gets_GET_method_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\n'
    result = parse_request(request_line)
    print(result)

    assert result['method'] == 'GET'

def test_parse_request_gets_uri_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\n'
    result = parse_request(request_line)

    assert result['uri'] == '/path/to/example.com'

def test_parse_request_gets_http_version_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1\r\n'
    result = parse_request(request_line)

    assert result['http_version'] == 'HTTP/1.1'