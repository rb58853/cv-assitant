from src.api.auth.master_key_generation import set_master_key
from database.security.generate_key import set_cryptography_key

master_key = set_master_key()
cryptography_key = set_cryptography_key()

