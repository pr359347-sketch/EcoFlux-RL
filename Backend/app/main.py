import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
STREAM_INTERVAL = 1.0

from app.routes.simulation import router as simulation_router
from app.websocket.manager import manager
from app.services.simulation_service import simulation_service


app = FastAPI(
    title="EcoTwin Backend API",
    description="Backend API for urban carbon dispersal simulation",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "EcoTwin Backend is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(simulation_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            if simulation_service.get_state()["connected_to_sumo"]:
                simulation_service.step()

            state = simulation_service.get_state()

            await manager.send_personal_message(
                {
                    "type": "simulation_update",
                    "simulation_id": state["simulation_id"],
                    "status": state["status"],
                    "data": {
                        "simulation_time": state["simulation_time"],
                        "vehicle_count": state["vehicle_count"],
                        "connected_to_sumo": state["connected_to_sumo"]
                    },
                    "timestamp": state["timestamp"]
                },
                websocket
            )

            await asyncio.sleep(STREAM_INTERVAL)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
