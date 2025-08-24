from app.server import HttpServer


def main(host: str, port: int, *, reuse_port: bool = True):
    with HttpServer(host, port, reuse_port=reuse_port) as server:
        server.start()


if __name__ == "__main__":
    main(host="localhost", port=4221, reuse_port=True)
