from fastapi.routing import APIRouter
from fastapi import WebSocket
import logging
from ..app.chat.chat import Chat

router = APIRouter(prefix='/api/v1', tags=['Api v1'])


@router.websocket('/open_chat')
async def open_chat_ws(websocket: WebSocket):
    await websocket.accept()
    logging.info(f'Client Connected to Websocket: {websocket.client.host}')
    chat = Chat()
    try:
        while True:
            query = await websocket.receive_text()
            response = await chat.send_query(query)
            await websocket.send_text(response)
    except Exception as e:
        logging.error(f'Connection with client closed ({e})')
