from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import WebSocket, Depends
import logging
import json
from ..app.chat.chat import Chat
from src.services.github_service.github_ import GithubAPI
from src.database.api_client import (
    set_user_data,
    register_user,
    get_user_key,
    get_user_token,
    get_user_repo,
)
import asyncio


router = APIRouter(prefix="/api/v1", tags=["Api v1"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/healt")
async def healt():
    return {"status": "healtly"}


@router.websocket("/open_chat")
async def open_chat_ws(websocket: WebSocket):
    await websocket.accept()
    logging.info(f"Client Connected to Websocket: {websocket.client.host}")
    user = await websocket.receive_text()
    print(f"user: {user}")
    chat = Chat()
    await websocket.send_text("connected")

    try:
        while True:
            query = await websocket.receive_text()
            response = await chat.send_query(query)
            response["response"]
            # TODO esto es solo temporal, despues se debe estandarizar el response
            await websocket.send_text(json.dumps(response))
            if "state" in response:
                raise Exception(response["message"])
    except Exception as e:
        logging.error(f"Connection with client closed ({e})")


@router.get("/data/user/generate/{username}/{reponame}")
async def reaload_repo_data(
    username: str,
    reponame: str,
    token: str = Depends(oauth2_scheme),
    overwrite=False,
):
    """
    Regenera la informacion de un usuario desde github
    """

    github = GithubAPI(user=username, repo=reponame, github_key=token)
    projects = asyncio.run(github.get_user_projects())
    info = asyncio.run(github.get_user_info())

    data = info
    data["projects"] = projects

    github.save_data(data)


@router.get("/data/users/load/{username}")
async def get_repo_data(username: str):
    reponame = get_user_repo(username)
    token = get_user_token(username)

    print(f"repo: {reponame}")
    print(f"token: {token}")

    github = GithubAPI(user=username, repo=reponame, github_key=token)
    data = github.load_data()
    set_user_data(user="rb58853", data=data)

    return {"status": "ok"}


@router.get("/data/cryptography/reload-key")
async def get_repo_info(key: str = Depends(oauth2_scheme)):
    """
    Esto es para el caso que cambies de api_key en criptografia
    """
    return {"status": "not impemented"}


@router.get("/data/users/register/{username}/{reponame}")
async def register_user_endpoint(
    username: str, reponame: str, token: str = Depends(oauth2_scheme)
):
    key = register_user(username, reponame, token)

    return {"status": "ok", "data": {"key": key}}
