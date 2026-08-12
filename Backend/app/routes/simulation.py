from fastapi import APIRouter

from app.services.simulation_service import simulation_service


router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"]
)


@router.post("/start")
def start_simulation():
    state = simulation_service.start()

    return {
        "message": "Simulation started",
        **state
    }


@router.post("/stop")
def stop_simulation():
    state = simulation_service.stop()

    return {
        "message": "Simulation stopped",
        **state
    }


@router.post("/reset")
def reset_simulation():
    state = simulation_service.reset()

    return {
        "message": "Simulation reset",
        **state
    }


@router.get("/status")
def get_simulation_status():
    return simulation_service.get_state()