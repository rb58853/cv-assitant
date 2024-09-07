from cryptography.fernet import Fernet
import os


def write_key(new_key):
    new_key = new_key.decode()
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir, ".env")

    new_lines = []
    with open(file_path, "r+") as file:
        lines = file.readlines()
        crypto_line = False
        for line in lines:
            if line.startswith("CRYPTOGRAPHY_KEY"):
                new_lines.append(f"CRYPTOGRAPHY_KEY = {new_key}")
                crypto_line = True
            else:
                new_lines.append(line)

        if not crypto_line:
            new_lines.append(f"CRYPTOGRAPHY_KEY={new_key}")

    with open(file_path, "w") as file:
        file.writelines(new_lines)


key = Fernet.generate_key()
write_key(key)
