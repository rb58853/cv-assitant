from src.app.openai_.gpt import GPT
from src.database.config import DataConfig
from src.database.data import data
from src.database.irs import irs


class Chat:
    def __init__(self, user=DataConfig.DefaultUser) -> None:
        self.gpt: GPT = GPT(info=data.get_info(user))
        self.history = []
        self.max_history_len = 5

    async def send_query(self, query):
        return self.process_query(query)

    def process_query(self, query):
        self.history.append({"role": "user", "content": query})
        self.history = self.history[: self.max_history_len * 2]
        response = self.gpt.conversation(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response

    def get_query_objetive(self, query):
        pass

    def process_projects(self, query):
        pass
