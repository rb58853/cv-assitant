from src.app.github_service.github_ import GithubAPI
import asyncio

github = GithubAPI(user="rb58853", repo="rb58853")

projects = asyncio.run(github.get_user_projects())
info = github.get_user_info()

data = info
data["projects"] = projects

github.save_data(data)
