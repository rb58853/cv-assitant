from client import APIClient
from env import GITHUB_USER
import asyncio


client = APIClient()


def chating(user=GITHUB_USER):
    clear_console()
    return asyncio.run(client.websocket_chat(user=user))

chating()