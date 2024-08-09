import requests
import asyncio
import websockets
import json

class APIClient:
    def __init__(
        self,
        http_url: str = "http://127.0.0.1:8000",
        ws_url="ws://127.0.0.1:8000",
        port: str = "8000",
    ) -> None:
        self.http_url = f"{http_url}"
        self.ws_url = f"{ws_url}"
        self.port = port

    async def websocket_chat(self, user):
        uri = f"{self.ws_url}/api/v1/open_chat"
        config = user
        # config = json.dumps({"store_name": store_name, "chat_id": str(chat_id)})

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
