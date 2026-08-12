from pydantic import BaseModel
from typing import Optional


class SimulationStatus(BaseModel):
    status: str
    simulation_id: Optional[str] = None


class SimulationUpdate(BaseModel):
    type: str = "simulation_update"
    simulation_id: Optional[str] = None
    status: str
    timestamp: float
    data: dict = {}