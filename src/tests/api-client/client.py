import requests
import asyncio
import websockets
import json
from requests.exceptions import RequestException

class APIClient:
    def __init__(
        self,
        http_url: str = "http://127.0.0.1:8000/api/v1",
        ws_url="ws://127.0.0.1:8000/api/v1",
        port: str = "8000",
    ) -> None:
        self.http_url = f"{http_url}"
        self.ws_url = f"{ws_url}"
        self.port = port

    def load_data(self, username, reponame, token):
        """
        Realiza una llamada al endpoint de GitHub y devuelve la información del repositorio.

        Args:
            base_url (str): URL base del servidor FastAPI
            username (str): Nombre de usuario del propietario del repositorio
            reponame (str): Nombre del repositorio
            token (str): Token de acceso de GitHub

        Returns:
            dict: Información del repositorio si la llamada es exitosa
        """
        url = f"{self.http_url}/data/users/load/{username}/{reponame}"

        # Configurar los encabezados con el token de GitHub
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Si la respuesta es exitosa, devolvemos los datos del repositorio
            return response.json()

        except RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None


    async def websocket_chat(self, user):
        uri = f"{self.ws_url}/api/v1/open_chat"
        config = user

        async with websockets.connect(uri, ping_interval=None) as websocket:
            # Enviar un mensaje al servidor
            await websocket.send(config)
            # Esperar y recibir un mensaje del servidor
            response = await websocket.recv()
            print(f"Respuesta del servidor: {response}")

            while True:
                try:
                    query = input("> ")
                    await websocket.send(query)
                    # print(f"> {query}")

                    response = await asyncio.wait_for(websocket.recv(), timeout=11120)
                    # response = await websocket.recv()
                    try:
                        response = json.loads(response)
                        print(f"< {response['response']}")
                    except:
                        print(f"< {response}")

                except Exception as e:
                    print(e)
                    break
