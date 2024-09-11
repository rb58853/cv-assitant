from api_client.client import APIClient
from env import GITHUB_USER, USER_KEY


client = APIClient()


def update(user=GITHUB_USER, user_key=USER_KEY):
    return client.update_data(user, user_key=user_key)


print(update())
