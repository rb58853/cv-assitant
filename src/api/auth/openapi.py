from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

class CustomOpenAPI:
    def __init__(self):
        pass

    def __call__(self, app: FastAPI):
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title = "FlowyChat API",
            version = "1.0.0",
            description = "Custom OpenAPI schema",
            routes = app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "APIKeyHeader": {
                "type": "apiKey",
                "name": "API-KEY",
                "in": "header"
            }
        }

        for path in openapi_schema['paths'].values():
            for method in path.values():
                method["security"] = [{"APIKeyHeader": []}]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema    