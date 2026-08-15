from time import time
from uuid import uuid4

from app.simulation.state import simulation_state
from app.simulation.sumo_client import sumo_client


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
        """
        Advance the SUMO simulation by one step
        and update the application state.
        """

        if not sumo_client.connected:
            raise RuntimeError("SUMO is not running.")

        sumo_client.simulation_step()

        simulation_state.update_time(
            sumo_client.get_time()
        )

        return self.get_state()

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