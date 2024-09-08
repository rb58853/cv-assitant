from typing import Any
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from starlette.routing import Match

from http import HTTPStatus
from src.config.logger_config import get_logger
from src.config.config import ConfigServer

from src.database.api_client import get_key
import requests

logger = get_logger(__name__)


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next) -> Response:

        logger.info(f"Request Path: {req.url.path}")
        logger.info(f"Request Scope Type: {req.scope['type']}")

        # if req.scope["type"] != "http":
        #     return

        if in_non_secure_endpoint(req):
            logger.info(f"Path {req.url.path} doesnt need authorization")
            return await call_next(req)

        params = Params(req)
        username = params.get_param("username")

        if username is None:
            # no hay username, no hay que autenticar nada
            return await call_next(req)

        api_key = req.headers.get("API-KEY")

        if not match_key(api_key, username):
            return JSONResponse(
                content={"detail": "Unauthorized API KEY"},
                status_code=HTTPStatus.UNAUTHORIZED,
            )

        response = await call_next(req)
        return response


def match_key(key, username):
    return key == get_key(username)


def in_non_secure_endpoint(req):
    for path in ConfigServer.PREX_NON_SECURE_PATHS:
        return req.url.path.startswith(path)


class Params:
    def __init__(self, req) -> None:
        self.req = req
        self.path_params = self.get_path_params()

    def get_path_params(self) -> Any:
        path_params = {}
        routes = self.req.app.router.routes
        for route in routes:
            match, scope = route.matches(self.req)
            if match == Match.FULL:
                path_params = scope["path_params"]
        return path_params

    def get_param(self, paramname):
        return self.path_params[paramname] if paramname in self.path_params else None
