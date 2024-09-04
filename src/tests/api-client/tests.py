import os
GITHUB_KEY = os.environ.get("GITHUB_KEY")

def clear_console():
    if os.name == "nt":  # Para Windows
        _ = os.system("cls")
    else:  # Para Unix/Linux
        _ = os.system("clear")


from client import APIClient
import asyncio

client = APIClient()


def chating(user="rb58853"):
    clear_console()
    return asyncio.run(client.websocket_chat(user=user))


def load_data(user="rb58853", repo="rb58853", token=GITHUB_KEY):
    client.load_data(user, repo, token)


print(load_data())
