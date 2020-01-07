class Connection:

    RECEIVING_REQUEST = 'RECEIVING_REQUEST'
    SENDING_RESPONSE = 'SENDING_RESPONSE'

    def __init__(self, address, socket):
        self.address = address
        self.socket = socket
        self.data = b''
        self.state = Connection.RECEIVING_REQUEST

        self.socket.setblocking(False)

    def send(self, response):
        len_bytes_sent = self.socket.send(response)
        return len_bytes_sent

    def close(self):
        self.socket.close()
