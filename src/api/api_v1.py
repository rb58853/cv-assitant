from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import WebSocket, Depends
import logging
import json
from ..app.chat.chat import Chat
from src.app.github_service.github_ import GithubAPI, GitHubConfig
from database.api.api import save_data
import asyncio


router = APIRouter(prefix="/api/v1", tags=["Api v1"])


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
            #TODO esto es solo temporal, despues se debe estandarizar el response
            await websocket.send_text(json.dumps(response))
            if 'state' in response:
                raise Exception (response['message'])
    except Exception as e:
        logging.error(f"Connection with client closed ({e})")


@router.post("/data/user/reload")
def reload_user_data(github_user, github_repo, override=False, git_token=None):
    """
    Regenera la informacion de un usuario desde github
    """

    github = GithubAPI(user="rb58853", repo="rb58853", github_key=git_token)
    projects = asyncio.run(github.get_user_projects())
    info = asyncio.run(github.get_user_info())

    data = info
    data["projects"] = projects

    github.save_data(data)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/data/users/load/{username}/{reponame}")
async def get_repo_info(
    username: str, reponame: str, token: str = Depends(oauth2_scheme)
):
    print(f"username: {username}")
    print(f"repo: {reponame}")
    print(f"token: {token}")

    github = GithubAPI(user=username, repo=reponame, github_key=token)
    data = github.load_data()
    save_data(user='rb58853', data=data)

    return {"status": "ok"}
