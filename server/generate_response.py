from os import scandir
from .response import Response

BODY_SUCCESS = '<h1>Hello World</h1>\r\n'
BODY_NOT_FOUND = '<h1>Page not found</h1>\r\n'
def generate_response(request, path_to_serve):
    body = None
    headers = None
    if request.uri == '/':
        status_code = 200

        if request.method == 'GET' or 'HEAD':
            body = create_html_body(path_to_serve)
            body += '\r\n'

        headers = [
            'Content-Type: text/html',
            f'Content-Length: {len(body)}'
        ]
    else:
        status_code = 404
        headers = [
            'Content-Type: text/html',
            f'Content-Length: {len(BODY_NOT_FOUND)}'
        ]
        body = BODY_NOT_FOUND
    if request.method == 'GET':
        response = Response(status_code, headers, body)
    elif request.method == 'HEAD':
        response = Response(status_code, headers, None)
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

def create_html_body(path):
    contents = get_contents_from_dir(path)
    html = f'<h1>{path}</h1><table><tbody>'

    for content in contents:
        if "/" in content:
            href = content[:-1]
        else:
            href = content
        html += f'<tr><td><a href="{href}">{content}</a></td></tr>'

    html += '</tbody></table>'
    return html

def read_file_contents(path_to_file):
    with open(path_to_file) as file:
        read_contents = file.read()
        return read_contents
