from api_client.client import APIClient
from utils.utils import clear_console
from env import GITHUB_USER, USER_KEY
import asyncio


client = APIClient()


def chating(user=GITHUB_USER, api_key=USER_KEY):
    clear_console()
    return asyncio.run(client.websocket_chat(user=user, api_key=api_key))


chating()
