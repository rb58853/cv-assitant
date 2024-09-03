from src.app.openai_.gpt.gpt import GPT
from src.database.config import UserDataConfig
from src.database.irs import irs
import json


class Chat:
    def __init__(self, user=UserDataConfig.DefaultUser) -> None:
        self.gpt: GPT = GPT(user=user)
        self.history = []
        self.max_history_len = 5
        self.user = user

    async def send_query(self, query):
        return self.process_query(query)

    def process_query(self, query):
        self.history.append({"role": "user", "content": query})
        self.history = self.history[: self.max_history_len * 2]

        query_fields = self.gpt.select_fields_from_query(self.history)

        # query_type = self.get_query_type(self.history)
        # if query_type["type"] == "projects":
        #     return self.process_projects(self.history)

        response = self.gpt.conversation(self.history, query_fields)
        self.history.append({"role": "assistant", "content": response})
        return {"response": response, "projects": {}}

    def get_query_type(self, history):
        query_type = self.gpt.identifique_query(history)
        return query_type

    def process_projects(self, history):
        keywords = None  # TODO esto es para el caso que se pueda usar embeddings
        projects = irs.get_documents_from_query(query=keywords, user=self.user)
        ids = self.gpt.end_irs(projects=projects, history=history)["projects"]
        projects = [p for p in projects.values() if p["id"] in ids]
        response = self.gpt.conversation(self.history, projects=projects)
        self.history.append({"role": "assistant", "content": response})

        if len(projects):
            return response
        else:
            return {"response": response, "projects": {}}
