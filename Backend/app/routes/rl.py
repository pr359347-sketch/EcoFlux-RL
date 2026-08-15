from fastapi import APIRouter

from app.services.rl_service import rl_service


router = APIRouter(
    prefix="/rl",
    tags=["Reinforcement Learning"]
)


@router.post("/initialize")
def initialize_rl():
    return rl_service.initialize()


@router.post("/action")
def get_rl_action(state: dict):
    return rl_service.get_action(state)


@router.post("/reset")
def reset_rl():
    return rl_service.reset()