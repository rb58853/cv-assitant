from database.api.actions import Get, Set


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
    return Get(user).key()


def register(user, repo, token):
    Set(user).register(repo, token)
    return get_key(user)
