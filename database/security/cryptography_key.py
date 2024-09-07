from cryptography.fernet import Fernet

key = Fernet.generate_key()
# cipher_suite = Fernet(key)
cipher_suite = Fernet('mi abuela en tanga')

message = "Hola, mundo!"
encrypted_message = cipher_suite.encrypt(message.encode())
decrypted_message = cipher_suite.decrypt(encrypted_message).decode()

print(f"Mensaje original: {message}")
print(f"Mensaje cifrado: {encrypted_message}")
print(f"Mensaje descifrado: {decrypted_message}")
