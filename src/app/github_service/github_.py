import markdown_to_json
from github import Github
from src.app.openai_.gpt.gpt import InfoGeneration
from src.config.config import GitHubConfig
import logging
import json


class GithubAPI:
    def __init__(self, user, repo, github_key=GitHubConfig.GITHUB_KEY) -> None:
        self.g = (
            Github(github_key)
            if github_key is not None
            else Github(GitHubConfig.GITHUB_KEY)
        )
        self.gptg = InfoGeneration()
        self.user = user
        self.user_repo = f"github.com/{user}/{repo}"
        self.short_repo = f"{user}/{repo}"

    async def get_user_info(self):
        info = {}

        async def get_file_info(file):
            md = file.decoded_content.decode("utf-8")
            dictified = await self.gptg.decode_md(md)

            for key in dictified:
                if len(dictified[key]):
                    info[key] = dictified[key]

        try:
            repo = self.g.get_repo(self.short_repo)
        except:
            logging.error(f"unfound repo {self.user_repo}")
            return None

        files = repo.get_contents("assistant/info")
        for content_file in files:
            if content_file.type == "file" and content_file.name[-3:].lower() == ".md":
                await get_file_info(content_file)

        return info

    async def get_user_projects(self):
        def get_project_md(repo, name):
            try:
                file = repo.get_contents(f"assistant/projects/{name}.md")
                return file.decoded_content.decode("utf-8")
            except:
                logging.warning(
                    f"unfound assistant/projects/{name}.md in repo {self.user_repo}"
                )
                return ""

        try:
            repo = self.g.get_repo(self.short_repo)
        except:
            logging.warning(f"unfound repo {self.user_repo}")
            return {}

        file = repo.get_contents("assistant/projects.json")
        projects = json.loads(file.decoded_content.decode("utf-8"))

        try:
            file = repo.get_contents("assistant/config.json")
            config = json.loads(file.decoded_content.decode("utf-8"))
            base_fields = config["projects"]["base_fields"]
        except:
            logging.warning(f"unfound assistant/config.json in repo {self.user_repo}")
            base_fields = []

        my_projects = []
        for project in projects:
            md = get_project_md(repo, project["id"])
            my_projects.append(
                await self.get_repo_info(
                    id=project["id"],
                    repo=project["repo"],
                    md=md,
                    base_fields=base_fields,
                )
            )
        return my_projects

    async def get_repo_info(self, id, repo=None, md="", base_fields=[]):
        repo_name = repo
        if repo:
            repo = repo.replace("github.com/", "").replace("https://", "")
            try:
                repo = self.g.get_repo(repo)
            except:
                logging.error(f"unfound repo {repo_name}")
                return None

            try:
                file = repo.get_contents("info.md")
            except:
                logging.warning(f"unfound info.md in repo {repo_name}.")
                return None

            work = file.decoded_content.decode("utf-8") + f"\n\n{md}"
        else:
            work = md

        result = await self.gptg.decode_work(work, base_fields)
        result["id"] = id
        result["github_repo"] = repo_name
        return result

    def save_data(self, json_var):
        repo = self.g.get_repo(self.short_repo)
        try:
            file = repo.get_contents("assistant/auto/data.json")

            content_file = repo.update_file(
                path="assistant/auto/data.json",
                message="Crear un nuevo archivo",
                content=json.dumps(json_var),
                sha=file.sha,
            )
            return content_file

        except:
            try:
                repo = self.g.get_repo(self.short_repo)
                content_file = repo.create_file(
                    path="assistant/auto/data.json",
                    message="Crear un nuevo archivo",
                    content=json.dumps(json_var),
                )
                return content_file
            except:
                logging.error(f"unfound repo {self.user_repo}")
                return False

    def load_data(self):
        try:
            repo = self.g.get_repo(self.short_repo)
        except:
            logging.error(f"unfound repo {self.user_repo}")
            return None

        file = repo.get_contents("assistant/auto/data.json")
        return json.loads(file.decoded_content.decode("utf-8"))
