import markdown_to_json
from github import Github
from src.app.openai_.gpt.gpt import InfoGeneration
from src.config.config import GitHubConfig
import logging
import json

g = Github(GitHubConfig.GITHUB_KEY)


class GithubAPI:
    def __init__(self, user, repo) -> None:
        self.gptg = InfoGeneration()
        self.user = user
        self.user_repo = f"github.com/{user}/{repo}"
        self.short_repo = f"{user}/{repo}"

    def get_user_info(self):
        info = {}

        try:
            repo = g.get_repo(self.short_repo)
        except:
            logging.error(f"unfound repo {self.user_repo}")
            return None

        files = repo.get_contents("assistant/info")
        for content_file in files:
            if content_file.type == "file" and content_file.name[-3:].lower() == ".md":
                temp = content_file.decoded_content.decode("utf-8")
                dictified = markdown_to_json.dictify(temp)

                for key in dictified:
                    if len(dictified[key]):
                        info[key] = dictified[key]

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
            repo = g.get_repo(self.short_repo)
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
                repo = g.get_repo(repo)
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
        return result
