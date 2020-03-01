from server.request import Request
from server.generate_response import generate_response
import pytest

@pytest.mark.focus
def test_generate_response_for_HEAD_request():
    request = Request('HEAD', '/', None, None, None)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 22\r\n\r\n'
    assert generate_response(request) == expected_result
