class FakeSocket:

    def __init__(self):
        self.sendBuffer = b''
        self.blocking = True
        self.closed = False

    def setblocking(self, is_blocking):
        self.blocking = is_blocking

    def send(self, response):
        if (self.closed):
            raise Exception('Connection closed')
        else:
            self.sendBuffer += response
            return self.sendBuffer

    def close(self):
        self.closed = True
