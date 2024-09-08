from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from http import HTTPStatus
from src.config.logger_config import get_logger
from src.config.config import ConfigServer

import requests

logger = get_logger(__name__)


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next) -> Response:

        logger.info(f"Request Path: {req.url.path}")
        logger.info(f"Request Scope Type: {req.scope['type']}")

        api_key = req.headers.get("API-KEY")
        logger.info(f"Recibed api-key: {api_key}")

        logger.info(f"path_params: {req.path_params}")
        logger.info(f"query_params: {req.query_params}")
        logger.info(f"query_params: {req._query_params}")


        # print(req._query_params)

        # if req.scope["type"] != "http":
        #     return

        # if req.url.path in ConfigServer.NON_SECURE_PATHS:
        #     return await call_next(req)

        # api_key = req.headers.get("API_KEY")

        # key_response = requests.get(
        #     f"{ConfigServer.API_KEY_CHECK_URL}/{api_key}"
        # ).json()

        # if not key_response["success"]:
        #     return JSONResponse(
        #         content={"detail": "Unauthorized or invalid API key"},
        #         status_code=HTTPStatus.FORBIDDEN,
        #     )

        # if key_response["data"]["active"] != 1:
        #     return JSONResponse(
        #         content={"detail": "API key is not active"},
        #         status_code=HTTPStatus.FORBIDDEN,
        #     )

        # if key_response["data"]["type"] != "secret":
        #     return JSONResponse(
        #         content={"detail": "API key is not secret"},
        #         status_code=HTTPStatus.FORBIDDEN,
        #     )

        response = await call_next(req)
        return response
