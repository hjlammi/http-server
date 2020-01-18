import socket
import selectors
from .connection import Connection
sel = selectors.DefaultSelector()

HOST = "127.0.0.1"
PORT = 8000

RESPONSE = '''HTTP/1.1 200 OK\r
Content-Type: text/html\r
Content-Length: 14\r
\r
<h1>jee</h1>\r
'''

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
                events = selectors.EVENT_READ | selectors.EVENT_WRITE
                sel.register(sock, events, data=connection)
            else:
                connection = key.data
                if mask & selectors.EVENT_READ and connection.state == Connection.RECEIVING_REQUEST:
                    recv_data = connection.socket.recv(1024)  # Should be ready to read
                    if recv_data:
                        print("recv_data", recv_data)
                        connection.data += recv_data
                        if b'\r\n\r\n' in recv_data:
                            connection.send(RESPONSE.encode())
                    else:
                        print("closing connection to", connection.address)
                        sel.unregister(connection.socket)
                        connection.close()
                if mask & selectors.EVENT_WRITE and connection.state == Connection.SENDING_RESPONSE:
                    connection.socket.send(RESPONSE.encode())  # Should be ready to write
                    sel.unregister(connection.socket)
                    connection.close()

# Starts sending response to the client after the whole request has been received
def request_received_callback(connection):
    connection.send(RESPONSE.encode())

def connection_closed_callback():
    pass

if __name__ == "__main__":
    main()
