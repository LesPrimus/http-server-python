from http import HTTPStatus
from os import PathLike

from app.models import Response
from app.models.request import Request
from app.server import HttpServer
from app.router import Router
from app.utils import get_command_line_args, read_file, write_file

router = Router()


def get_files(request: Request, **params) -> Response:
    try:
        body = read_file(request, **params)
        return Response(
            status=HTTPStatus.OK, content_type="application/octet-stream", body=body
        )
    except KeyError:
        return Response(status=HTTPStatus.BAD_REQUEST)
    except FileNotFoundError:
        return Response(status=HTTPStatus.NOT_FOUND)


def post_files(request: Request, **params) -> Response:
    try:
        write_file(request, **params)
        return Response(status=HTTPStatus.CREATED)
    except KeyError:
        return Response(status=HTTPStatus.BAD_REQUEST)
    except FileNotFoundError:
        return Response(status=HTTPStatus.NOT_FOUND)


@router.register(r"/files/(?P<filename>\w+)")
def files(request: Request, **params):
    match request.method:
        case "GET":
            return get_files(request, **params)
        case "POST":
            return post_files(request, **params)
        case _:
            return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


@router.register(r"/user-agent")
def user_agent(request: Request, **params):
    return Response(
        status=HTTPStatus.OK, body=request.headers.get("User-Agent", "Unknown")
    )


@router.register(r"/echo(/(?P<string>\w+))?")
def echo(request: Request, **params):
    print(request.headers, "//////")
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
