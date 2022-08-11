from typing import List, Dict
from fastapi import WebSocket

from managers.ChatManager import ChatManager


class ChatConnectionManager:
    def __init__(self):
        self.connections = {}
        self.chatManager = ChatManager()

    async def connect(self, websocket: WebSocket, token, id):
        await websocket.accept()
        self.connections[websocket] = [token, id]

    def disconnect(self, websocket: WebSocket):
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
        print(token, chat_id)
        print(self.connections)
        self.chatManager.postMessage(token=token, id=chat_id, text=message)
        messages = self.chatManager.getAllMessages(token=token, id=chat_id)
        for con in self.connections:
            print(self.connections[con])
            if self.connections[con][1] == chat_id:
                if messages is None:
                    messages = []
                await con.send_json(data=messages)