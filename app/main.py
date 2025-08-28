from http import HTTPStatus

from app.models import Response
from app.models.request import Request
from app.server import HttpServer
from app.router import Router

router = Router()


@router.register(r"/user-agent")
def user_agent(request: Request, **params):
    return Response(
        status=HTTPStatus.OK, body=request.headers.get("User-Agent", "Unknown")
    )


@router.register(r"/echo(/(?P<string>\w+))?")
def echo(request: Request, **params):
    return Response(status=HTTPStatus.OK, body=params["string"])


@router.register(path=r"/")
def home(request: Request, **params):
    return Response(status=HTTPStatus.OK)


def main(host: str, port: int, *, reuse_port: bool = True):
    with HttpServer(host, port, router, reuse_port=reuse_port) as server:
        server.start()


if __name__ == "__main__":
    main(host="localhost", port=4221, reuse_port=True)
