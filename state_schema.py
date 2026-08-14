from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class VehicleState:
    id: str
    x: float
    y: float
    speed: float
    co2: float
    waiting_time: float


@dataclass
class TrafficLightState:
    id: str
    phase: int
    state: str


@dataclass
class SimulationState:
    step: int
    vehicles: list[VehicleState]
    total_co2: float
    total_waiting_time: float
    traffic_lights: list[TrafficLightState]

    def to_dict(self) -> dict[str, Any]:
        """Convert simulation state into JSON-friendly dictionary."""
        return asdict(self)