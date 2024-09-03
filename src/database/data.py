from src.database.config import DataConfig
import logging

if DataConfig.Local:
    from src.database.api_client import LocalData as API
else:
    from src.database.api_client import Requests as API


class Data:
    def __init__(self) -> None:
        self.info = {}

    def get_info(self, user):
        if DataConfig.RamData and user in self.info:
            return self.info[user]
        else:
            data = API.get_info(user)
            if DataConfig.RamData:
                self.info[user] = data
            return data

    def forget_user(self, user):
        if DataConfig.RamData:
            try:
                self.info.pop(user, None)
                return True
            except:
                False

        return True

    def reload_user(self, user):
        if DataConfig.RamData:
            self.info[user] = API.get_info(user)
            if self.info[user] is None:
                logging.error(f"user {user} not found")
                return False

        return True

    def get_info_from_fields(self, user, fields):
        pass


data = Data()
