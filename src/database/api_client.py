import os
from database.api.api import get_field_info, get_info, get_fields_from_user


class LocalData:
    def get_info(user):
        return get_field_info(user, "information")

    def get_projects(user):
        return get_field_info(user, "projects")

    def get_user_data(user):
        return get_info(user)

    def get_field(user, field):
        return get_field_info(user, field)
    
    def get_user_fields(user):
        return get_fields_from_user(user)


class Requests:
    def get_info(user):
        pass

    def get_projects(user):
        pass

    def get_full_projects(user):
        pass

    def get_full_info(user):
        pass
