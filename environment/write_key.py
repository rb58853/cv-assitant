import os

def write_key_to_enviroment(key, name):
    # key = key.decode()
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir, ".env")

    new_lines = []
    with open(file_path, "r+") as file:
        lines = file.readlines()
        crypto_line = False
        for line in lines:
            if line.startswith(name):
                new_lines.append(f"{name} = {key}\n")
                crypto_line = True
            else:
                new_lines.append(line)

        if not crypto_line:
            new_lines.append(f"CRYPTOGRAPHY_KEY={key}")

    with open(file_path, "w") as file:
        file.writelines(new_lines)

