from typing import List, Dict
from fastapi import WebSocket

from managers.ChatManager import ChatManager


class ChatConnectionManager:
    def __init__(self):
        self.connections = {}
        self.chatManager = ChatManager()

    async def connect(self, websocket: WebSocket, token, id):
        resp = self.chatManager.getChat(token, id)
        await websocket.accept()
        if resp[0] is True:
            self.connections[websocket] = [token, id]
        else:
            await websocket.close()

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
        del self.connections[websocket]

    def getInfo(self, websocket):
        return self.connections[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)

    async def send_in_chat(self, message: str, websocket: WebSocket):
        chat_id = self.connections[websocket][1]
        token = self.connections[websocket][0]
        message = self.chatManager.postMessage(token=token, id=chat_id, text=message)
        for con in self.connections:
            if self.connections[con][1] == chat_id:
                if message is None:
                    message = {
                        "text": "websocket: some problem occurred"
                    }
                await con.send_json(data=message)