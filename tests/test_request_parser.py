from server.request_parser import parse_request
import pytest

def test_parse_request_gets_GET_method_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1'
    result = parse_request(request_line)

    assert result['startline']['method'] == 'GET'

def test_parse_request_gets_uri_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1'
    result = parse_request(request_line)

    assert result['startline']['uri'] == '/path/to/example.com'

def test_parse_request_gets_http_version_from_the_request():
    request_line = 'GET /path/to/example.com HTTP/1.1'
    result = parse_request(request_line)

    assert result['startline']['http_version'] == 'HTTP/1.1'
