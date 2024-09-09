from typing import Any
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from starlette.routing import Match

from http import HTTPStatus
from src.config.logger_config import get_logger
from src.config.config import ConfigServer

from src.database.api_client import get_key
import os

logger = get_logger(__name__)


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next) -> Response:

        logger.info(f"Request Path: {req.url.path}")
        logger.info(f"Request Scope Type: {req.scope['type']}")

        # if req.scope["type"] != "http":
        #     return

        if in_non_secure_endpoint(req):
            return await call_next(req)

        params = Params(req)
        username = params.get_param("username")

        if username is None and not in_master_secure_endpoint(req):
            # no hay username ni hay que usar el master, no hay que autenticar nada
            return await call_next(req)

        recived_key = req.headers.get("API-KEY")
        api_key = get_key(username)

        if in_master_secure_endpoint(req):
            recived_key = req.headers.get("MASTER-API-KEY")
            api_key = os.environ.get("MASTER_KEY")

        print(f"recived key: {recived_key}")
        print(f"api key: {api_key}")

        if not match_key(api_key, recived_key):
            return JSONResponse(
                content={"detail": "Unauthorized API KEY"},
                status_code=HTTPStatus.UNAUTHORIZED,
            )

        response = await call_next(req)
        return response


def match_key(recived_key, key):
    return key == recived_key


def in_non_secure_endpoint(req):
    for path in ConfigServer.PREX_NON_SECURE_PATHS:
        if req.url.path.startswith(path):
            return True
    return False


def in_master_secure_endpoint(req):
    for path in ConfigServer.PREX_MASTER_SECURE_PATHS:
        if req.url.path.startswith(path):
            return True
    return False


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
