import pathlib
from http import HTTPStatus
from os import PathLike

from app.models import Response
from app.models.request import Request
from app.server import HttpServer
from app.router import Router
from app.utils import get_command_line_args

router = Router()


@router.register(r"/files/(?P<filename>\w+)")
def files(request: Request, **params):
    try:
        filename = params["filename"]
    except KeyError:
        return Response(status=HTTPStatus.BAD_REQUEST)

    try:
        directory = pathlib.Path(request.state["directory"])
    except KeyError:
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    try:
        with pathlib.Path(directory / filename).open("r") as f:
            body = f.read()
    except FileNotFoundError:
        return Response(status=HTTPStatus.NOT_FOUND)

    return Response(
        status=HTTPStatus.OK, content_type="application/octet-stream", body=body
    )


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


def main(
    host: str, port: int, *, reuse_port: bool = True, directory: PathLike | None = None
):
    with HttpServer(
        host, port, router, reuse_port=reuse_port, directory=directory
    ) as server:
        server.start()


if __name__ == "__main__":
    args = get_command_line_args()
    main(host="localhost", port=4221, reuse_port=True, directory=args.directory)
