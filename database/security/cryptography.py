import os
from cryptography.fernet import Fernet


def encode(key):
    cryptography_key = os.environ.get("CRYPTOGRAPHY_KEY")
    cipher_suite = Fernet(cryptography_key)
    return cipher_suite.encrypt(key.encode()).decode()


def decode(key):
    cryptography_key = os.environ.get("CRYPTOGRAPHY_KEY")
    cipher_suite = Fernet(cryptography_key)
    return cipher_suite.decrypt(key).decode()
