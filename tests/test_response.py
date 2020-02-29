from server.response import Response

def test_serialize_200_ok_response_without_headers_and_body():
    response = Response(200)
    expected_result = b'HTTP/1.1 200 OK\r\n'
    assert response.serialize() == expected_result

def test_serialize_204_no_content_response_without_headers_and_body():
    response = Response(204)
    expected_result = b'HTTP/1.1 204 No Content\r\n'
    assert response.serialize() == expected_result

def test_serialize_200_ok_response_with_html_body():
    body = '<h1>jee</h1>\r\n'
    content_type = 'Content-Type: text/html'
    content_length = f'Content-Length: {len(body)}'
    headers = [content_type, content_length]
    response = Response(200, headers, body)
    expected_result = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 14\r\n\r\n<h1>jee</h1>\r\n'
    assert response.serialize() == expected_result
