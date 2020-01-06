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
        self.socket.send(response)

    def close(self):
        self.socket.close()
