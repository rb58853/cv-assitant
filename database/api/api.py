from database.api.actions import Get, Set
from ..security.cryptography import decode, encode


def save_data(user, data):
    try:
        Set(user).user_data(data=data)
        return True
    except:
        return False


def load_data(user):
    try:
        return Get(user).user_data(user)
    except:
        return None


def set_key(user, key):
    return Set(user).key(key)


def get_key(user):
    pass
