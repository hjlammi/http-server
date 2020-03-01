from .response import Response

BODY = '<h1>Hello World</h1>\r\n'
def generate_response(request):
    if request.uri == '/':
        status_code = 200
        headers = [
            'Content-Type: text/html',
            f'Content-Length: {len(BODY)}'
        ]
    response = Response(status_code, headers, None)
    return response.serialize()
