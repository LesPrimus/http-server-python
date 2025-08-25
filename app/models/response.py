from dataclasses import dataclass, field
from http import HTTPStatus

__all__ = ("Response",)


@dataclass
class Response:
    status: HTTPStatus
    body: str = field(default_factory=str)
