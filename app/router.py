from collections.abc import Callable
from dataclasses import dataclass, field

__all__ = ("Router",)

from http import HTTPStatus

from app.models import Request, Response


@dataclass
class Router:
    routes: dict[str, Callable] = field(default_factory=dict)

    def register(self, path: str):
        def decorator(handler: Callable):
            self.routes[path] = handler
            return handler

        return decorator

    def route(self, request: Request):
        for path, handler in self.routes.items():
            if path == request.path:
                return handler(request)
        return Response(status=HTTPStatus.NOT_FOUND)
