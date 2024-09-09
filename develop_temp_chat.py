from src.app.chat.chat import Chat
from src.utils.clean_terminal import clean
from src.services.github_service.github_ import GithubAPI
import asyncio
from src.database.api_client import (
    set_user_data,
    register_user,
    register_user,
    get_user_token,
    get_user_repo,
)


def chating():
    chat = Chat()
    clean()

    while True:
        query = input(">")
        print(f"<{chat.process_query(query)}")


def register(user, repo, token):
    return register_user(user, repo, token)


def update_git_data(username):
    reponame = get_user_repo(username)
    token = get_user_token(username)

    github = GithubAPI(user=username, repo=reponame, github_key=token)
    projects = asyncio.run(github.get_user_projects())
    info = asyncio.run(github.get_user_info())

    data = info
    data["projects"] = projects

    github.save_data(data)

update_git_data('rb58853')