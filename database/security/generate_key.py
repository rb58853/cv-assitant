from cryptography.fernet import Fernet

try:
    from environment.write_key import write_key_to_enviroment

    write = True
except:
    write = False


def fernet_key():
    return Fernet.generate_key().decode()


def set_cryptography_key():
    key = fernet_key()
    if write:
        write_key_to_enviroment(key=key, name="CRYPTOGRAPHY_KEY")
    return key


def generate_user_key():
    return fernet_key()
