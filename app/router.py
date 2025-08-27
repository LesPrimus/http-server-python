import re
from collections.abc import Callable
from dataclasses import dataclass, field

__all__ = ("Router",)

from http import HTTPStatus

from app.models import Request, Response


@dataclass
class Router:
    routes: dict[re.Pattern[str], Callable] = field(default_factory=dict)

    def register(self, path: str):
        def decorator(handler: Callable):
            self.routes[re.compile(path)] = handler
            return handler

        return decorator

    def route(self, request: Request):
        for path, handler in self.routes.items():
            if match := path.fullmatch(request.path):
                return handler(request, **match.groupdict())
        return Response(status=HTTPStatus.NOT_FOUND)
