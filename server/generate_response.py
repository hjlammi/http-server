from .response import Response

BODY_SUCCESS = '<h1>Hello World</h1>\r\n'
BODY_NOT_FOUND = '<h1>Page not found</h1>\r\n'
def generate_response(request, path_to_serve):
    body = None
    headers = None
    if request.uri == '/':
        status_code = 200
        headers = [
            'Content-Type: text/html',
            f'Content-Length: {len(BODY_SUCCESS)}'
        ]

        if request.method == 'GET':
            body = BODY_SUCCESS
    else:
        status_code = 404
        headers = [
            'Content-Type: text/html',
            f'Content-Length: {len(BODY_NOT_FOUND)}'
        ]
        body = BODY_NOT_FOUND
    response = Response(status_code, headers, body)
    return response.serialize()
