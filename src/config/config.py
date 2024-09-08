import os


class ConfigGPT:
    MODEL_PRICE = {
        "gpt-3.5-turbo": {
            "input": 0.5 / 1000000,
            "output": 1.5 / 1000000,
        },
        "gpt-4o-mini": {
            "input": 0.15 / 1000000,
            "output": 0.60 / 1000000,
        },
    }

    DEFAULT_MODEL_NAME = "gpt-4o-mini"

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class RetrievalConfig:
    # Campos usados para filtrar proyectos por la query. Estos campos se matchean con NLP para usar los campos reales de los proyectos
    PROJECTS_KEYS = ["id", "title", "keywords", "skills", "programing_languages"]


class GitHubConfig:
    # Token de github
    GITHUB_KEY = os.environ.get("GITHUB_KEY")
    GITHUB_USER = os.environ.get("GITHUB_USER")
    GITHUB_REPO = os.environ.get("GITHUB_REPO")


class GenerationConfig:
    # Campos obligatorios para la generacion de proyectos o trabajos
    work_fields = ["title", "keywords", "skills"]
