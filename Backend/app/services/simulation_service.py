from time import time
from uuid import uuid4

from app.simulation.state import simulation_state
from app.simulation.sumo_client import sumo_client
from app.services.rl_service import rl_service


class SimulationService:

    def start(self):
        # Prevent starting another session while one is already running
        if sumo_client.connected:
            raise RuntimeError("Simulation is already running.")

        simulation_id = f"sim_{uuid4().hex[:8]}"

        # Start SUMO through TraCI
        sumo_client.start()

        # Update application state
        simulation_state.start(simulation_id)
        simulation_state.set_sumo_connection(True)

        # Get initial SUMO simulation time
        simulation_state.update_time(
            sumo_client.get_time()
        )

        return self.get_state()

    def stop(self):
        # Stop SUMO connection
        sumo_client.close()

        # Update application state
        simulation_state.stop()
        simulation_state.set_sumo_connection(False)

        return self.get_state()

    def reset(self):
        # Close existing SUMO connection if active
        sumo_client.close()

        # Reset application state
        simulation_state.reset()

        return self.get_state()

    def step(self):
        # Advance SUMO simulation by one step
        if not sumo_client.connected:
            raise RuntimeError("SUMO is not running.")

        sumo_client.simulation_step()

        # Update simulation time
        simulation_state.update_time(
            sumo_client.get_time()
        )

        # Get current simulation state
        state = self.get_state()

        # Ask RL service for the next action
        action = rl_service.get_action({
            "simulation_time": state["simulation_time"],
            "vehicle_count": state["vehicle_count"],
            "connected_to_sumo": state["connected_to_sumo"]
        })
        sumo_client.apply_traffic_light_action(
            action["action"]
        )

        # Store RL action in simulation state
        simulation_state.set_rl_action(
            action["action"]
        )

        return {
            **self.get_state(),
            "rl_action": action["action"]
        }

    def get_state(self):
        state = simulation_state.get_state()

        return {
            **state,
            "vehicle_count": (
                sumo_client.get_vehicle_count()
                if sumo_client.connected
                else 0
            ),
            "timestamp": time()
        }


simulation_service = SimulationService()