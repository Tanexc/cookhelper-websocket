from typing import Union

import uvicorn as uvicorn
from fastapi import WebSocket, FastAPI, Depends, Query
from fastapi.responses import HTMLResponse
from managers.ConnectionManager import ChatConnectionManager

app = FastAPI()

manager = ChatConnectionManager()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://cookhelper-ws.herokuapp.com/ws/chat/1/?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


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