from typing import Any

import requests
from constants.Constants import *


class ChatManager:
    CHAT_GET = "api/chat/get/"
    CHAT_POST_MES = "api/chat/post/message/"
    CHAT_GET_MES = "api/message/get/"

    def getChat(self, token: str, id: int) -> tuple[bool, Any]:
        response = requests.get(API_URL + self.CHAT_GET + f"?token={token}&id={id}").json()
        if response["status"] == 400:
            return True, response["chat"]
        else:
            return False, response["status"]

    def postMessage(self, token: str, id: int, text: str):
        response = requests.post(API_URL + self.CHAT_POST_MES + f"?token={token}&id={id}&text={text}").json()
        if response["status"] == 400:
            return True
        else:
            return False

    def getAllMessages(self, token: str, id: int):
        ret = []
        resp = self.getChat(token, id)
        if resp[0] is True:
            messages = resp[1]["messages"]
        else:
            return None
        for mid in messages.split():
            response = requests.get(API_URL + self.CHAT_GET_MES + f"?token={token}&id={mid}&chat-id={id}").json()
            ret.append(response["chat-message"])
        return ret