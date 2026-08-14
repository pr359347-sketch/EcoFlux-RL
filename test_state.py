import traci

from simulation_state import get_simulation_state


SUMO_CFG = "citygrid.sumocfg"


# Start SUMO
traci.start([
    "sumo",
    "-c",
    SUMO_CFG
])


# Run simulation
for step in range(10):

    traci.simulationStep()

    state = get_simulation_state(step)

    print(
        f"Step {step} | "
        f"Vehicles: {len(state.vehicles)} | "
        f"CO2: {state.total_co2:.2f} | "
        f"Waiting: {state.total_waiting_time:.2f} | "
        f"Traffic Lights: {len(state.traffic_lights)}"
    )


# Close SUMO
traci.close()

print("State test completed!")