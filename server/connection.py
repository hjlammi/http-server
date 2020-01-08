class Connection:

    RECEIVING_REQUEST = 'RECEIVING_REQUEST'
    SENDING_RESPONSE = 'SENDING_RESPONSE'

    def __init__(self, address, socket):
        self.address = address
        self.socket = socket
        self.data = b''
        self.send_buffer = b''
        self.state = Connection.RECEIVING_REQUEST
        self.response_left = None

        self.socket.setblocking(False)

    def send(self, response):
        self.send_buffer += response
        self.state = Connection.SENDING_RESPONSE
        len_bytes_sent = self.socket.send(response)
        self.response_left = response[len_bytes_sent:]
        return len_bytes_sent

    def close(self):
        self.socket.close()
