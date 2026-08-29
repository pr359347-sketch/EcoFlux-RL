from fastapi import APIRouter, HTTPException

from app.services.simulation_service import simulation_service


router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"]
)


@router.post("/start")
def start_simulation():
    try:
        state = simulation_service.start()

        return {
            "message": "Simulation started",
            **state
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/stop")
def stop_simulation():
    try:
        state = simulation_service.stop()

        return {
            "message": "Simulation stopped",
            **state
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/reset")
def reset_simulation():
    try:
        state = simulation_service.reset()

        return {
            "message": "Simulation reset",
            **state
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/status")
def get_simulation_status():
    return simulation_service.get_state()


@router.post("/step")
def step_simulation():
    try:
        state = simulation_service.step()

        return {
            "message": "Simulation stepped",
            **state
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )