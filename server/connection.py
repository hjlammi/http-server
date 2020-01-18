class Connection:

    RECEIVING_REQUEST = 'RECEIVING_REQUEST'
    SENDING_RESPONSE = 'SENDING_RESPONSE'
    CLOSED = 'CLOSED'

    def __init__(self, address, socket, connection_closed_callback):
        self.address = address
        self.socket = socket
        self.data = b''
        self.send_buffer = b''
        self.recv_buffer = b''
        self.buffer_size = 1024
        self.request_received_callback = None
        self.connection_closed_callback = connection_closed_callback
        self.state = None

        self.socket.setblocking(False)

    def receive(self, request_received_callback, bufsize):
        self.buffer_size = bufsize
        self.request_received_callback = request_received_callback
        self.state = Connection.RECEIVING_REQUEST

    def send(self, response):
        if (self.state == Connection.CLOSED):
            raise Exception('Connection closed')
        else:
            self.send_buffer += response
            self.state = Connection.SENDING_RESPONSE

    def update(self):
        if (self.state == Connection.RECEIVING_REQUEST):
            received_bytes = self.socket.recv(self.buffer_size)
            if received_bytes:
                self.recv_buffer += received_bytes
                if b'\r\n\r\n' in self.recv_buffer:
                    self.request_received_callback(self)
            else:
                self.close()
        elif (self.state == Connection.SENDING_RESPONSE):
            response = self.send_buffer
            len_bytes_sent = self.socket.send(response)
            self.send_buffer = response[len_bytes_sent:]

    def close(self):
        self.state = Connection.CLOSED
        self.socket.close()
        self.connection_closed_callback(self.socket)
