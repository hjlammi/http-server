from os import scandir, path
import magic
from .response import Response

def generate_response(request, path_to_serve):
    body = None
    headers = None
    response = None

    path_to_resource = path_to_serve + request.uri
    if path.isdir(path_to_resource) and not path_to_resource.endswith('/'):
        return generate_301_response(request);
    if is_a_valid_resource(path_to_resource):
        status_code = 200

        if request.method == 'GET' or 'HEAD':
            if path.isfile(path_to_resource):
                mime_type = magic.from_file(path_to_resource, mime=True)
                if (mime_type):
                    return generate_response_for_a_file_request(path_to_resource, mime_type)
            else:
                body = list_dir_contents_in_html(path_to_resource, path_to_serve)
                body += b'\r\n'
                headers = [
                    'Content-Type: text/html',
                    f'Content-Length: {len(body)}'
                ]

    else:
        return generate_404_response(request)
    if request.method == 'GET':
        response = Response(status_code, headers, body)
    elif request.method == 'HEAD':
        response = Response(status_code, headers, None)
    response_bytestr = response.serialize()
    return response_bytestr

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

def list_dir_contents_in_html(path_to_resource, path_to_serve):
    contents = get_contents_from_dir(path_to_resource)
    relative_path = get_relative_path(path_to_resource, path_to_serve)
    html = f'<h1>{relative_path}</h1><table><tbody>'

    for content in contents:
        if "/" in content:
            href = content[:-1]
        else:
            href = content
        html += f'<tr><td><a href="{href}">{content}</a></td></tr>'

    html += '</tbody></table>'
    return html.encode()

def read_file_contents_in_bytes(path_to_file):
    with open(path_to_file, 'rb') as file:
        return file.read()

def is_a_valid_resource(path_to_resource):
    if path.isfile(path_to_resource):
        return True
    elif path.isdir(path_to_resource):
        return True
    else:
        return False

def get_relative_path(path_to_resource, path_to_serve):
    if path_to_serve.endswith('/'):
        path_to_serve = path_to_serve[:-1]
    if path_to_resource.endswith('/'):
        path_to_resource = path_to_resource[:-1]
    relative_path = path_to_resource.replace(path_to_serve, '')
    if not relative_path:
        relative_path = '/'
    return relative_path

def generate_301_response(request):
    headers = [
        'Content-Length: 0',
        f'Location: {request.uri}/'
    ]
    response = Response(301, headers, None, None)
    return response.serialize()

def generate_404_response(request):
    response_body = b'<h1>Page not found</h1>\r\n'
    headers = [
        f'Content-Length: {len(response_body)}',
        f'Location: {request.uri}/'
    ]
    response = Response(404, headers, response_body)
    return response.serialize()

def generate_response_for_a_file_request(path_to_resource, mime_type):
    size = path.getsize(path_to_resource)
    body = read_file_contents_in_bytes(path_to_resource)
    headers = [
        f'Content-Type: {mime_type}',
        f'Content-Length: {size}'
    ]
    response = Response(200, headers, body)
    return response.serialize()
