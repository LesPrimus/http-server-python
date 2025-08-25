from http import HTTPStatus

from app.models import Response
from app.models.request import Request
from app.server import HttpServer
from app.router import Router

router = Router()


@router.register(path="/")
def home(request: Request):
    return Response(status=HTTPStatus.OK)


def main(host: str, port: int, *, reuse_port: bool = True):
    with HttpServer(host, port, router, reuse_port=reuse_port) as server:
        server.start()


if __name__ == "__main__":
    main(host="localhost", port=4221, reuse_port=True)
