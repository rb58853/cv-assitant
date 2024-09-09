from src.services.openai_.gpt.gpt import GPT, GPTChat, GPTRetrieval
from src.database.config import UserDataConfig
from src.database.irs import irs
import json


class Chat:
    def __init__(self, user=UserDataConfig.DefaultUser) -> None:
        self.gpt: GPTChat = GPTChat(user=user)
        self.gptRetrieval: GPTRetrieval = GPTRetrieval()
        self.history = []
        self.max_history_len = 5
        self.user = self.gpt.user_data

    def current_price(self):
        return self.gptRetrieval.current_price + self.gpt.current_price

    async def send_query(self, query):
        return self.process_query(query)

    def process_query(self, query):
        if self.user.data is None:
            return {
                "response": f"You({self.user.username}) has not data.",
                "projects": [],
                "state": "error",
                "message": f"User {self.user.username} doesnt exist in database",
            }

        self.history.append({"role": "user", "content": query})
        self.history = self.history[: self.max_history_len * 2]

        query_fields = self.gpt.select_fields_from_query(self.history)

        query_type = self.get_query_type(self.history)
        if query_type["type"] == "projects":
            return self.process_projects(self.history, query_fields)

        response = self.gpt.conversation(self.history, query_fields)
        self.history.append({"role": "assistant", "content": response})
        return {"response": response, "projects": {}}

    def get_query_type(self, history):
        query_type = self.gpt.identifique_query(history)
        return query_type

    def process_projects(self, history, fields):
        if "projects" not in fields:
            fields.append("projects")

        keywords = None  # TODO esto es para el caso que se use embeddings
        projects = irs.get_projects_from_query(
            query=keywords, user_data=self.gpt.user_data
        )

        ids = self.gptRetrieval.end_irs(projects=projects, history=history)["projects"]
        projects = [p for p in projects if p["id"] in ids]
        response = self.gpt.conversation(self.history, projects=projects, fields=fields)
        assistant_message = "response['response']: " + "\n".join(
            [f'{index+1}- {p["title"]}' for index, p in enumerate(projects)]
        )

        self.history.append({"role": "assistant", "content": assistant_message})

        if len(projects):
            return response
        else:
            return {"response": response, "projects": {}}
