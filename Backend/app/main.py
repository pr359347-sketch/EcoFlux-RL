from fastapi import FastAPI, WebSocket, WebSocketDisconnect

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
            data = await websocket.receive_text()

            state = simulation_service.get_state()

            await manager.send_personal_message(
                {
                    "type": "simulation_update",
                    "simulation_id": state["simulation_id"],
                    "status": state["status"],
                    "data": {
                        "message": data
                    },
                    "timestamp": state["timestamp"]
                },
                websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)