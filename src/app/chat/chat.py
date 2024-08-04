from src.app.openai_.gpt import GPT
from data.data import info


class Chat:
    def __init__(self, gpt: GPT = GPT(info=info)) -> None:
        self.gpt: GPT = gpt
        self.history = []
        self.max_history_len = 5

    async def send_query(self, query):
        pass

    def process_query(self, query):
        self.history.append({"role": "user", "content": query})
        self.history = self.history[: self.max_history_len * 2]
        response = self.gpt.conversation(self.history)
        self.history.append({"role": "assistant", "content": response})
        return response
