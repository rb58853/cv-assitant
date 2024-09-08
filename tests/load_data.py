from api_client.client import APIClient
from env import GITHUB_USER


client = APIClient()


def load_data(user=GITHUB_USER):
    return client.load_data(user)


print(load_data())
