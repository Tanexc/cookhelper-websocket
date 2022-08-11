from typing import Union

import uvicorn as uvicorn
from fastapi import WebSocket, FastAPI, Depends, Query
from fastapi.responses import HTMLResponse
from managers.ConnectionManager import ChatConnectionManager

app = FastAPI()

manager = ChatConnectionManager()


@app.websocket("/ws/chat/{id}/")
async def chat_websocket_endpoint(
        websocket: WebSocket,
        id: str,
        token: Union[str, None] = None
):
    await manager.connect(websocket, token, id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_in_chat(message=data, websocket=websocket)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    uvicorn.run(app)