from dotenv import load_dotenv
from .auth.openapi import CustomOpenAPI
from .auth.middleware import APIKeyMiddleware

load_dotenv()

from fastapi import FastAPI
from .api_v1 import router as router_v1

app = FastAPI()
app.openapi = lambda: CustomOpenAPI(app)()
app.add_middleware(APIKeyMiddleware)

app.include_router(router_v1)
