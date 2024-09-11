from api_client.client import APIClient
from env import GITHUB_USER, USER_KEY


client = APIClient()


def load_data(user=GITHUB_USER, user_key=USER_KEY):
    return client.load_data(user, user_key=user_key)


print(load_data())
