from api_client.client import APIClient
from env import GITHUB_USER, GITHUB_REPO, GITHUB_KEY


client = APIClient()


def register(user=GITHUB_USER,repo =GITHUB_REPO, token = GITHUB_KEY):
    return client.register(username = user, git_repo=repo, git_token= token)


print(register())
