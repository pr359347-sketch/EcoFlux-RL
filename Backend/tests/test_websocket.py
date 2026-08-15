import asyncio
import websockets


async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:
        print("WebSocket connected!")

        for i in range(5):
            response = await websocket.recv()

            print(f"Update {i + 1}:")
            print(response)

        print("WebSocket live streaming test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_websocket())