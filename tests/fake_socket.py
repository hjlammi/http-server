class FakeSocket:

    BUFFER_SIZE = 4

    def __init__(self):
        self.recv_buffer = b''
        self.send_buffer = b'test'
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

    def recv(self, bufsize):
        bytes_to_send = self.send_buffer[:bufsize]
        self.send_buffer = self.send_buffer[bufsize:]
        return bytes_to_send

    def close(self):
        self.closed = True
