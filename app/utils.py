import argparse
import pathlib
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Request, Response


def get_headers(*args) -> dict:
    return dict([tuple(arg.split(":", 1)) for arg in args if arg])  # noqa


def get_command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="Directory path", type=Path)
    return parser.parse_args()


def read_file(request: "Request", **params) -> str:
    filename = params["filename"]
    directory = pathlib.Path(request.state["directory"])

    with pathlib.Path(directory / filename).open("r") as f:
        return f.read()


def write_file(request: "Request", **params) -> int:
    filename = params["filename"]
    directory = pathlib.Path(request.state["directory"])
    body = request.body

    with pathlib.Path(directory / filename).open("w") as f:
        return f.write(body)
