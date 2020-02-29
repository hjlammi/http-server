import socket
import selectors
from .connection import Connection
from .response import Response
sel = selectors.DefaultSelector()

HOST = "127.0.0.1"
PORT = 8000

def main():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print('listening on', (HOST, PORT))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                sock, addr = key.fileobj.accept()  # Should be ready to read
                print('accepted connection from', addr)
                connection = Connection(addr, sock, connection_closed_callback)
                connection.receive(request_received_callback, 1024)
                events = selectors.EVENT_READ
                sel.register(sock, events, data=connection)
            else:
                connection = key.data
                connection.update()

# Starts sending response to the client after the whole request has been received
def request_received_callback(connection):
    body = '<h1>jee</h1>\r\n'
    content_type = 'Content-Type: text/html'
    content_length = f'Content-Length: {len(body)}'
    headers = [content_type, content_length]
    response = Response(200, headers, body)
    connection.send(response.serialize())
    events = selectors.EVENT_WRITE
    sel.modify(connection.socket, events, data=connection)

# Unregisters socket after the connection has been closed
def connection_closed_callback(socket):
    sel.unregister(socket)

if __name__ == "__main__":
    main()
