from time import time

from app.simulation.state import simulation_state


class SimulationService:

    def start(self):
        simulation_id = "sim_001"

        simulation_state.start(simulation_id)

        return self.get_state()

    def stop(self):
        simulation_state.stop()

        return self.get_state()

    def reset(self):
        simulation_state.reset()

        return self.get_state()

    def get_state(self):
        state = simulation_state.get_state()

        return {
            **state,
            "timestamp": time()
        }


simulation_service = SimulationService()