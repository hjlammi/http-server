from .response import Response

BODY = '<h1>Hello World</h1>\r\n'
def generate_response(request):
    body = None
    if request.uri == '/':
        status_code = 200
        headers = [
            'Content-Type: text/html',
            f'Content-Length: {len(BODY)}'
        ]

        if request.method == 'GET':
            body = BODY
    response = Response(status_code, headers, body)
    return response.serialize()
