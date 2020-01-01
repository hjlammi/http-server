import socket
import selectors
from .connection import Connection
sel = selectors.DefaultSelector()

HOST = "127.0.0.1"
PORT = 8000

# State
RECEIVING_REQUEST = 'RECEIVING_REQUEST'
SENDING_RESPONSE = 'SENDING_RESPONSE'

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
                conn, addr = key.fileobj.accept()  # Should be ready to read
                print('accepted connection from', addr)
                conn.setblocking(False)
                connection = Connection(addr)
                events = selectors.EVENT_READ | selectors.EVENT_WRITE
                sel.register(conn, events, data=connection)
            else:
                sock = key.fileobj
                connection = key.data
                if mask & selectors.EVENT_READ and connection.state == RECEIVING_REQUEST:
                    recv_data = sock.recv(1024)  # Should be ready to read
                    if recv_data:
                        print("recv_data", recv_data)
                        connection.data += recv_data
                        if b'\r\n\r\n' in recv_data:
                            connection.state = SENDING_RESPONSE
                    else:
                        print("closing connection to", connection.address)
                        sel.unregister(sock)
                        sock.close()
                if mask & selectors.EVENT_WRITE and connection.state == SENDING_RESPONSE:
                    sent = sock.send(RESPONSE.encode())  # Should be ready to write
                    print("Sent", sent)
                    sel.unregister(sock)
                    sock.close()

if __name__ == "__main__":
    main()
