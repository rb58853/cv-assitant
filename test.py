from src.app.github_service.github_ import GithubAPI
import asyncio

github = GithubAPI(user="rb58853", repo="rb58853")
asyncio.run(github.get_user_projects())
