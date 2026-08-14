import asyncio
import websockets


async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:
        print("WebSocket connected!")

        await websocket.send("Hello EcoTwin")

        response = await websocket.recv()

        print("Server response:")
        print(response)


if __name__ == "__main__":
    asyncio.run(test_websocket())