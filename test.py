from src.app.github_service.github_ import GithubAPI
import asyncio

github = GithubAPI('rb58853')
# asyncio.run(github.get_repo_info("https://github.com/rb58853/NavAgent-AI"))
asyncio.run(github.get_user_projects())