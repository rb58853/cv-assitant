def getRepo(path):
    pass


from github import Github

# Configurar el token de acceso personal
g = Github("")

# Acceder al repositorio por nombre o ID
repo = g.get_repo("nombre-del-repositorio")

# Obtener los archivos del repositorio
files = repo.get_contents("")

for content_file in files:
    print(f"Nombre del archivo: {content_file.name}")
    print(f"Tamaño: {content_file.size} bytes")
    print(f"Tipo de contenido: {content_file.type}\n")