from server.request_parser import parse_request

class Connection:

    RECEIVING_REQUEST = 'RECEIVING_REQUEST'
    RECEIVING_BODY = 'RECEIVING_BODY'
    SENDING_RESPONSE = 'SENDING_RESPONSE'
    CLOSED = 'CLOSED'

    def __init__(self, address, socket, connection_closed_callback):
        self.address = address
        self.socket = socket
        self.send_buffer = b''
        self.recv_buffer = b''
        self.buffer_size = 1024
        self.request_received_callback = None
        self.connection_closed_callback = connection_closed_callback
        self.state = None
        self.request_body = None
        self.parsed_request = None

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
                    request_str = self.recv_buffer
                    split_request = request_str.split(b'\r\n\r\n')
                    self.parsed_request = parse_request(split_request[0].decode('utf-8'))
                    if self.parsed_request.headers is not None:
                        if 'content-length' in self.parsed_request.headers:
                            self.state = Connection.RECEIVING_BODY
                            content_length = int(self.parsed_request.headers['content-length'])
                            body = split_request[1]
                            self.request_body = body[:content_length]
                        else:
                            # No content-length provided so we are not interested in message body
                            self.request_received_callback(self, self.parsed_request)
                    else:
                        # No headers, so we are not interested the message body
                        self.request_received_callback(self, self.parsed_request)
            else:
                self.close()
        elif (self.state == Connection.RECEIVING_BODY):
            content_length = int(self.parsed_request.headers['content-length'])
            read_capacity_left = content_length
            received_bytes = self.socket.recv(self.buffer_size)
            if received_bytes:
                if (self.request_body):
                    read_req_body_len = len(self.request_body)
                    read_capacity_left = content_length - read_req_body_len
                self.request_body += received_bytes[:read_capacity_left]
                read_req_body_len = len(self.request_body)
                # Enough read of the body
                if (read_req_body_len == content_length):
                    self.request_received_callback(self)
            else:
                self.request_received_callback(self)
        elif (self.state == Connection.SENDING_RESPONSE):
            response = self.send_buffer
            len_bytes_sent = self.socket.send(response)
            if not len_bytes_sent:
                raise Exception('Socket connection broken')
            self.send_buffer = response[len_bytes_sent:]
            if not self.send_buffer:
                self.close()

    def close(self):
        self.state = Connection.CLOSED
        self.socket.close()
        self.connection_closed_callback(self.socket)
