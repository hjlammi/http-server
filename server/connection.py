class Connection:

    RECEIVING_REQUEST = 'RECEIVING_REQUEST'
    SENDING_RESPONSE = 'SENDING_RESPONSE'
    CLOSED = 'CLOSED'

    def __init__(self, address, socket):
        self.address = address
        self.socket = socket
        self.data = b''
        self.send_buffer = b''
        self.state = Connection.RECEIVING_REQUEST

        self.socket.setblocking(False)

    def send(self, response):
        if (self.state == Connection.CLOSED):
            raise Exception('Connection closed')
        else:
            self.send_buffer += response
            self.state = Connection.SENDING_RESPONSE

    def close(self):
        self.state = Connection.CLOSED
        self.socket.close()
