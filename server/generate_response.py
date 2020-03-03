from os import scandir
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

def get_contents_from_dir(path):
    dirs = []
    files = []
    with scandir(path) as scandir_iterator:
        for entry in scandir_iterator:
            if entry.is_dir():
                dirs.append(f'{entry.name}/')
            if entry.is_file():
                files.append(entry.name)
    files.sort()
    dirs.sort()
    dirs.extend(files)
    return dirs
