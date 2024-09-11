from dotenv import load_dotenv
load_dotenv()

from .auth.openapi import CustomOpenAPI
from .auth.middleware import APIKeyMiddleware
from fastapi import FastAPI, Request
from .api_v1 import router as router_v1

app = FastAPI()
app.openapi = lambda: CustomOpenAPI(app)()
app.add_middleware(APIKeyMiddleware)

app.include_router(router_v1)

