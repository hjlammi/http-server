from server.response import Response

def test_serialize_200_ok_response_without_headers_and_body():
    response = Response(200)
    expected_result = 'HTTP/1.1 200 OK\r\n'
    assert response.serialize() == expected_result

def test_serialize_204_no_content_response_without_headers_and_body():
    response = Response(204)
    expected_result = 'HTTP/1.1 204 No Content\r\n'
    assert response.serialize() == expected_result
