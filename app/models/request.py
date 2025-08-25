from dataclasses import dataclass
from http import HTTPMethod

__all__ = ("Request",)

from app.utils import get_headers


@dataclass
class Request:
    method: HTTPMethod
    path: str
    version: str
    headers: dict[str, str]
    body: str

    @classmethod
    def from_raw(cls, raw: str):
        request_line, *headers, body = raw.split("\r\n")
        method, path, version = request_line.split(" ")
        headers = get_headers(*headers)
        method = HTTPMethod(method)
        return cls(
            method=method,
            path=path,
            version=version,
            headers=headers,
            body=body,
        )
