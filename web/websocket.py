from asyncio import Lock
from collections import defaultdict

from starlette.websockets import WebSocket


class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(set)
        self.lock = Lock()

    async def connect(self, websocket: WebSocket, ticker_name: str):
        await websocket.accept()
        self.active_connections[ticker_name].add(websocket)

    async def disconnect(self, websocket: WebSocket):
        for ticker_name, websockets in self.active_connections.items():
            if websocket in websockets:
                print('removing websocket')
                websockets.remove(websocket)

    async def broadcast_ticker_value(self, ticker_name: str, value: int, timestamp: int):
        to_delete = []
        for ticker, connections in self.active_connections.items():
            if ticker_name == ticker:
                async with self.lock:
                    for connection in connections:
                        try:
                            await connection.send_json({'ticker': ticker_name, 'value': value, 'timestamp': timestamp})
                        except Exception as e:
                            to_delete.append(connection)
        for connection in to_delete:
            async with self.lock:
                await self.disconnect(connection)