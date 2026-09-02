import asyncio

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket
    ):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        disconnected = []

        async def send(connection: WebSocket):
            try:
                await asyncio.wait_for(
                    connection.send_json(message),
                    timeout=2.0
                )
            except Exception:
                disconnected.append(connection)

        await asyncio.gather(
            *(send(connection) for connection in self.active_connections)
        )

        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()