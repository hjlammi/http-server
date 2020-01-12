class FakeSocket:

    BUFFER_SIZE = 4

    def __init__(self):
        self.recv_buffer = b''
        self.blocking = True
        self.closed = False

    def setblocking(self, is_blocking):
        self.blocking = is_blocking

    def send(self, response):
        if (self.closed):
            raise Exception('Connection closed')
        else:
            read_bytes = response[:FakeSocket.BUFFER_SIZE]
            self.recv_buffer += read_bytes
            return len(read_bytes)

    def close(self):
        self.closed = True
