from database.api.utils import get_user_data, set_user_data


def save_data(user, data):
    try:
        set_user_data(user=user, data=data)
        return True
    except:
        return False


def get_info(user):
    try:
        return get_user_data(user)
    except:
        return None


# def get_field_info(user, field_name):
#     try:
#         return get_user_data(user)[field_name]
#     except:
#         return None


# def get_fields_from_user(user):
#     try:
#         return get_user_data(user).fields()
#     except:
#         return None
