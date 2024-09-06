from client import APIClient
from env import GITHUB_USER, GITHUB_REPO


client = APIClient()


def load_data(user=GITHUB_USER, repo=USER_REPO, token=GITHUB_KEY):
    return client.load_data(user, repo, token)


print(load_data())
