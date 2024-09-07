from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
from src.app.config.config import ConfigServer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from http import HTTPStatus
from src.app.config.logger_config import get_logger

import requests

logger = get_logger(__name__)

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next) -> Response:
        
        logger.info(f"Request Path: {req.url.path}")
        logger.info(f"Request Scope Type: {req.scope['type']}")
        
        if req.scope['type'] != 'http':
            return

        if req.url.path in ConfigServer.NON_SECURE_PATHS:
            return await call_next(req)
        
        api_key = req.headers.get("X-API_KEY")
        key_response = requests.get(f"{ConfigServer.API_KEY_CHECK_URL}/{api_key}").json()
        
        if not key_response["success"]:
            return JSONResponse(
                content={"detail": "Unauthorized or invalid API key"},
                status_code=HTTPStatus.FORBIDDEN
            )
            
        if key_response["data"]["active"] != 1:
            return JSONResponse(
                content={"detail": "API key is not active"},
                status_code=HTTPStatus.FORBIDDEN
            )

        if key_response["data"]["type"] != "secret":
            return JSONResponse(
                content={"detail": "API key is not secret"},
                status_code=HTTPStatus.FORBIDDEN
            )
        
        response = await call_next(req)
        return response


def generate_token(client_id, expires_delta: timedelta) -> str:    
    expire = datetime.utcnow() + expires_delta

    payload = {'client_id': client_id, 'exp': expire}
    encoded_jwt = jwt.encode(payload, ConfigServer.FLOWY_API_KEY, algorithm="HS256")

    return encoded_jwt