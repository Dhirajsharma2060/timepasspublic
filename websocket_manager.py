import asyncio
import json
import websockets
from typing import Dict, List, Union

class WebSocketManager:
    def __init__(self):
        self.connected_clients: List[websockets.WebSocketServerProtocol] = []

    async def register(self, websocket: websockets.WebSocketServerProtocol):
        self.connected_clients.append(websocket)
        print(f"New client connected. Total clients: {len(self.connected_clients)}")

    async def unregister(self, websocket: websockets.WebSocketServerProtocol):
        self.connected_clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(self.connected_clients)}")

    async def notify_clients(self, message: Dict[str, Union[str, Dict[str, int]]]):
        if self.connected_clients:
            message_json = json.dumps(message)
            await asyncio.wait([client.send(message_json) for client in self.connected_clients])

    async def producer_handler(self):
        while True:
            # Simulated data for illustration purposes
            voter_status = "Voted"
            party_votes = {"Party 1": 10, "Party 2": 15, "Party 3": 8}

            # Send updates to connected clients
            message = {"voter_status": voter_status, "party_votes": party_votes}
            await self.notify_clients(message)

            # Simulated delay before sending the next update
            await asyncio.sleep(5)
