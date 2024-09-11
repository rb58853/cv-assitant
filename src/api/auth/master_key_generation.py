from cryptography.fernet import Fernet

try:
    from environment.write_key import write_key_to_enviroment
    write = True
except:
    write = False



def fernet_key():
    return Fernet.generate_key().decode()


def set_master_key():
    master_key = fernet_key()
    if write:
        write_key_to_enviroment(key=master_key, name="MASTER_KEY")
    return master_key
