from database.api.actions import Get, Set


def save_data(user, data):
    try:
        Set(user).user_data(data=data)
        return True
    except:
        return False


def load_data(user):
    try:
        return Get(user).user_data()
    except:
        return None


def set_key(user, key):
    return Set(user).key(key)


def get_key(user):
    return Get(user).key()


def get_token(user):
    return Get(user).token()


def get_repo(user):
    return Get(user).repo()


def register(user, repo, token):
    return Set(user).register(repo, token)
