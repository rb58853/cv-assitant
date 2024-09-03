import os


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


chating("rb58853")

client.load_data("rb58853", "rb58853")
