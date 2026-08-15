import os
import traci


class SumoClient:
    def __init__(self):
        self.connected = False

        self.sumo_config_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "sumo",
                "simulation.sumocfg"
            )
        )

    def start(self):
        """
        Start SUMO and establish a TraCI connection.
        """

        if self.connected:
            return

        if not os.path.exists(self.sumo_config_path):
            raise FileNotFoundError(
                f"SUMO configuration not found: "
                f"{self.sumo_config_path}"
            )

        traci.start([
            "sumo",
            "-c",
            self.sumo_config_path,
            "--start",
            "--quit-on-end"
        ])

        self.connected = True

    def simulation_step(self):
        """
        Advance SUMO simulation by one step.
        """

        if not self.connected:
            raise RuntimeError("SUMO is not connected.")

        traci.simulationStep()

    def get_time(self):
        """
        Get current SUMO simulation time.
        """

        if not self.connected:
            raise RuntimeError("SUMO is not connected.")

        return traci.simulation.getTime()

    def get_vehicle_count(self):
        """
        Get number of vehicles currently in the simulation.
        """

        if not self.connected:
            raise RuntimeError("SUMO is not connected.")

        return traci.vehicle.getIDCount()

    def close(self):
        """
        Close the TraCI connection.
        """

        if self.connected:
            traci.close()
            self.connected = False


sumo_client = SumoClient()