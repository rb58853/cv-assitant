from api_client.client import APIClient
from env import GITHUB_USER, GITHUB_REPO, GITHUB_KEY, MASTER_KEY, VPS_HOST
import os

client = APIClient(vps= VPS_HOST)


def register(
    user=GITHUB_USER, repo=GITHUB_REPO, token=GITHUB_KEY, master_key=MASTER_KEY
):
    return client.register(
        username=user, git_repo=repo, git_token=token, master_key=master_key
    )


print(register())
