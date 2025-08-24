import socket
from http import HTTPStatus


class HttpServer:
    VERSION = "HTTP/1.1"
    CRLF = "\r\n"

    def __init__(self, host, port, *, reuse_port=True):
        self.host = host
        self.port = port
        self.reuse_port = reuse_port
        self.server_socket = self._create_socket()

    def _create_socket(self):
        return socket.create_server((self.host, self.port), reuse_port=self.reuse_port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start(self):
        try:
            print(f"Listening on {self.host}:{self.port}")
            while True:
                (client_socket, client_address) = self.server_socket.accept()
                self.handle_client(client_socket, client_address)

        except KeyboardInterrupt:
            print("Shutting down server...")
            self.close()

    def close(self):
        self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        request = client_socket.recv(1024)
        print(f"Received request: {request.decode()} from {client_address}")
        response = f"{self.VERSION} {HTTPStatus.OK.value} {HTTPStatus.OK.phrase}{self.CRLF}{self.CRLF}"
        client_socket.send(response.encode())
