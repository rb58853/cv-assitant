from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class CustomOpenAPI:
    def __init__(self, app: FastAPI):
        self.app = app

    def __call__(self):
        if self.app.openapi_schema:
            return self.app.openapi_schema

        openapi_schema = get_openapi(
            title="Assistant API",
            version="1.0.0",
            description="Custom OpenAPI schema with api-keys authorization",
            routes=self.app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "APIKeyHeader": {"type": "apiKey", "name": "API-KEY", "in": "header"},
            "MasterAPIKeyHeader": {
                "type": "apiKey",
                "name": "MASTER-API-KEY",
                "in": "header",
            },
        }

        for path in openapi_schema["paths"].values():
            for method in path.values():
                method["security"] = [{"APIKeyHeader": [], "MasterAPIKeyHeader": []}]

        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema
