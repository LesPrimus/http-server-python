from dataclasses import dataclass, field
from http import HTTPStatus

__all__ = ("Response",)


@dataclass
class Response:
    status: HTTPStatus
    body: str | bytes = field(default_factory=str)
    content_type: str = field(default="text/plain")
    content_encoding: str = field(default="")

    @property
    def content_length(self):
        return len(self.body.strip())
