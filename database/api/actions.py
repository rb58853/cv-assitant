import os
from .utils import write_json, open_json, write_fields
from ..security.cryptography import decode, encode

data_path = os.path.join(os.getcwd(), "database/data")
if not os.path.exists(data_path):
    os.makedirs(data_path, exist_ok=True)


class Set:
    def __init__(self, user) -> None:
        self.user = user

    def user_data(self, data):
        dir_path = os.path.join(data_path, f"{self.user}")
        path = os.path.join(dir_path, "data.json")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        os.makedirs(path, exist_ok=True)

        return write_json(path, data)

    def config_value(self, key, value):
        dir_path = os.path.join(data_path, f"{self.user}")
        path = os.path.join(dir_path, "config.json")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        os.makedirs(path, exist_ok=True)
        return write_fields(path, {key: value})

    def key(self, key):
        key = encode(key)
        return self.config_value(key="key", value=key)

    def token(self, token):
        token = encode(token)
        return self.config_value(key="token", value=token)

    def repo(self, repo):
        return self.config_value(key="repo", value=repo)

    def register(self, repo, token):
        key = encode("12345")
        token = encode(token)

        dir_path = os.path.join(data_path, f"{self.user}")
        path = os.path.join(dir_path, "config.json")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        return write_fields(path, {"key": key, "repo": repo, "token": token})


class Get:
    def __init__(self, user) -> None:
        self.user = user
        # self.key = self.key()
        # self.repo = self.repo()
        # self.token = self.token()

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
        return decode(self.config_value(key="key"))

    def token(self):
        return decode(self.config_value(key="token"))

    def repo(self):
        return self.config_value(key="repo")


class Migrations:
    def when_new_cryptography_key(previous_key):
        """
        En caso que se cambie la key del environmet de criptography entonces debes regenerar todo usando la key anterior, Si pierdes la key tendras que volver a subir el token y el api_key de cada usuario
        """
        pass
