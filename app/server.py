import logging
import socket

from app.models import Response
from app.models.request import Request
from app.router import Router

logger = logging.getLogger(__name__)


class HttpServer:
    VERSION = "HTTP/1.1"
    CRLF = "\r\n"
    BUFFER_SIZE = 1024

    def __init__(
        self, host: str, port: int, router: Router, *, reuse_port: bool = True
    ):
        self.host = host
        self.port = port
        self.router = router
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
        logger.info(f"Client {client_address[0]}:{client_address[1]}")
        raw_request = client_socket.recv(self.BUFFER_SIZE).decode()
        request = Request.from_raw(raw_request)
        response = self.router.route(request)
        self.send_response(response, to=client_socket)

    def get_headers(self, response: Response) -> str:
        return self.CRLF.join(
            [
                "Content-Type: text/plain",
                f"Content-Length: {len(response.body.strip())}",
            ]
        )

    def format_response(self, response: Response) -> bytes:
        return (
            f"{self.VERSION} {response.status.value} {response.status.phrase}{self.CRLF}"
            f"{self.get_headers(response)}{self.CRLF}{self.CRLF}"
            f"{response.body.strip()}"
        ).encode()

    def send_response(self, response: Response, *, to: socket.socket):
        print(self.format_response(response))
        to.send(self.format_response(response))
