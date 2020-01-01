class Connection:

    def __init__(self, address):
        self.address = address
        self.data = b''
        self.state = 'RECEIVING_REQUEST'
