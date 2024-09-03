from src.app.github_service.github_ import GithubAPI
from database.api.api import save_data
import asyncio

github = GithubAPI(user="rb58853", repo="rb58853")

projects = asyncio.run(github.get_user_projects())
info = asyncio.run(github.get_user_info())

data = info
data["projects"] = projects

github.save_data(data)

data = github.load_data()
save_data(user='rb58853', data=data)
