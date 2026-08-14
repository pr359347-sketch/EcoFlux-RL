from typing import Optional


class SimulationState:
    def __init__(self):
        self.status: str = "stopped"
        self.simulation_id: Optional[str] = None
        self.simulation_time: float = 0.0
        self.connected_to_sumo: bool = False

    def start(self, simulation_id: str):
        self.status = "running"
        self.simulation_id = simulation_id
        self.simulation_time = 0.0

    def stop(self):
        self.status = "stopped"

    def reset(self):
        self.status = "stopped"
        self.simulation_id = None
        self.simulation_time = 0.0
        self.connected_to_sumo = False

    def update_time(self, simulation_time: float):
        self.simulation_time = simulation_time

    def set_sumo_connection(self, connected: bool):
        self.connected_to_sumo = connected

    def get_state(self):
        return {
            "status": self.status,
            "simulation_id": self.simulation_id,
            "simulation_time": self.simulation_time,
            "connected_to_sumo": self.connected_to_sumo,
        }


simulation_state = SimulationState()