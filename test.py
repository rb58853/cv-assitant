from src.app.github_service.github_ import GithubAPI
from database.api.api import save_data
import asyncio

github = GithubAPI(user="rb58853", repo="rb58853")
data = github.load_data()
save_data(user='rb58853', data=data)
