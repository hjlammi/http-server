class Connection:

    RECEIVING_REQUEST = 'RECEIVING_REQUEST'
    SENDING_RESPONSE = 'SENDING_RESPONSE'
    CLOSED = 'CLOSED'

    def __init__(self, address, socket):
        self.address = address
        self.socket = socket
        self.data = b''
        self.send_buffer = b''
        self.recv_buffer = b''
        self.state = Connection.RECEIVING_REQUEST

        self.socket.setblocking(False)

    def receive(self, bufsize = 1024):
        self.recv_buffer += self.socket.recv(bufsize)

    def send(self, response):
        if (self.state == Connection.CLOSED):
            raise Exception('Connection closed')
        else:
            self.send_buffer += response
            self.state = Connection.SENDING_RESPONSE

    def update(self):
        response = self.send_buffer
        len_bytes_sent = self.socket.send(response)
        self.send_buffer = response[len_bytes_sent:]

    def close(self):
        self.state = Connection.CLOSED
        self.socket.close()
