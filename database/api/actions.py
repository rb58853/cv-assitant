import os
from utils import write_json, open_json, write_fields

data_path = os.path.join(os.getcwd(), "database/data")
os.makedirs(data_path, exist_ok=True)


class Set:
    def __init__(self, user) -> None:
        self.user = user

    def user_data(self, data):
        path = os.path.join(data_path, f"{self.user}/data.json")
        os.makedirs(path, exist_ok=True)
        return write_json(path, data)

    def config_value(self, key, value):
        path = os.path.join(data_path, f"{self.user}/config.json")
        os.makedirs(path, exist_ok=True)
        return write_fields(path, {key: value})

    def key(self, key):
        return self.config_value(user=self.user, key="key", value=key)

    def token(self, token):
        return self.config_value(user=self.user, key="token", value=token)

    def repo(self, repo):
        return self.config_value(user=self.user, key="repo", value=repo)


class Get:
    def __init__(self, user) -> None:
        self.self.user = user

    def user_data(self):
        path = os.path.join(data_path, f"{self.user}/data.json")
        return open_json(path)

    def config_value(self, key):
        path = os.path.join(data_path, f"{self.user}/config.json")
        try:
            config = open_json(path)
            return config[key]
        except:
            return None
        

    def key(self):
        return self.config_value(key="key")

    def token(self):
        return self.config_value(key="token")

    def repo(self):
        return self.config_value(key="repo")
