import socket

HOST = "127.0.0.1"
PORT = 8000
RESPONSE = '''HTTP/1.1 200 OK
Content-Type: text/html

<h1>jee</h1>
'''

def hello():
    return "hello"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print("Connected by", addr)
                conn.recv(1024)
                conn.sendall(RESPONSE.encode())

if __name__ == "__main__":
    main()
