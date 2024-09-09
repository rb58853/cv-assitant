from src.app.chat.chat import Chat
from ..utils.utils import clear_console
from src.services.github_service.github_ import GithubAPI
from ..env import GITHUB_USER, GITHUB_REPO, GITHUB_KEY

import asyncio
from src.database.api_client import (
    register_user,
    register_user,
    get_user_token,
    get_user_repo,
)

# EXECUTE THIS TESTS FROM ROOT PATH, FOR EXAMPLE THE FILE current_develop_time_test.py


def register(user=GITHUB_USER, repo=GITHUB_REPO, token=GITHUB_KEY):
    """
    ## User register
    This function has debug objetive
    ### USE
    **This function just can use from if is called from a root path, otherwise its will be broken**

    ### Inputs
    - `user`: username from github
    - `repo`: github repo with user information
    - `token`: github token with authorization to read repos

    ### Outputs
    - `api-key`: api-kry by using in our api
    """
    return register_user(user, repo, token)


def chating(user=GITHUB_USER):
    """
    This function just can use from if is called from a root path, otherwise its will be broken
    """
    chat = Chat(user=user)
    clear_console()

    while True:
        query = input(">")
        print(f"<{chat.process_query(query)}")


def update_git_data(username=GITHUB_USER):
    """
    This function just can use from if is called from a root path, otherwise its will be broken
    """
    reponame = get_user_repo(username)
    token = get_user_token(username)

    github = GithubAPI(user=username, repo=reponame, github_key=token)
    projects = asyncio.run(github.get_user_projects())
    info = asyncio.run(github.get_user_info())

    data = info
    data["projects"] = projects

    github.save_data(data)
