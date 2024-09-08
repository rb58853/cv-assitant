from src.app.chat.chat import Chat
from src.utils.clean_terminal import clean
from src.config.config import GitHubConfig
from src.database.api_client import register_user


def chating():
    chat = Chat()
    clean()

    while True:
        query = input(">")
        print(f"<{chat.process_query(query)}")


def register(user, repo, token):
    return register_user(user, repo, token)


key = register(
    GitHubConfig.GITHUB_USER, GitHubConfig.GITHUB_REPO, GitHubConfig.GITHUB_KEY
)
