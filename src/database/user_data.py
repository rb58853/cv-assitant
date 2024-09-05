from src.database.api_client import get_user_data


class UserData:
    def __init__(self, user) -> None:
        self.username = user
        self.load_data()

    def storage_data(self):
        # Analizar bien que pasa en memoria y si tiene sentido usar el storage en vez de la ram para este caso
        return get_user_data(self.username)

    def load_data(self):
        self.data = get_user_data(self.username)
        return self.data

    def get_info_from_fields(self, fields):
        return {key: self.data[key] for key in self.data if key in fields}

    def get_fields(self):
        return list(self.data.keys())
