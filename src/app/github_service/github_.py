import markdown_to_json
from github import Github
from src.app.openai_.gpt.gpt import InfoGeneration

from src.config.config import GitHubConfig
g = Github(GitHubConfig.GITHUB_KEY)

INFO = {}

def get_full_info(user):
    repo = g.get_repo(f"{user}/{user}")
    files = repo.get_contents("assistant")
    for content_file in files:
        if content_file.type == "file" and content_file.name[-3:].lower() == ".md":
            temp = content_file.decoded_content.decode("utf-8")
            dictified = markdown_to_json.dictify(temp)
            for key in dictified:
                if len(dictified[key]):
                    INFO[key] = dictified[key]

    files = repo.get_contents("assistant/projects")


def get_project_info(repo):
    repo = repo.replace("github.com/", "").replace("https://", "")
    repo = g.get_repo(repo)
    file = repo.get_contents("info.md")
    work = file.decoded_content.decode("utf-8")
    gpt = InfoGeneration()
    result = gpt.decode_work(work)
    return result



# get_full_info("rb58853")
