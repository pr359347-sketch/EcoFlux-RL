import traci
import csv

from simulation_state import get_simulation_state


# ---- Config ----

SUMO_CFG = "citygrid.sumocfg"
NUM_STEPS = 1000
OUTPUT_CSV = "simulation_log.csv"


# ---- Start SUMO ----

traci.start([
    "sumo",
    "-c",
    SUMO_CFG
])


# ---- Traffic lights ----

tls_ids = traci.trafficlight.getIDList()

print(
    f"Found {len(tls_ids)} traffic lights: {tls_ids}"
)


# ---- Open CSV file ----

with open(
    OUTPUT_CSV,
    mode="w",
    newline=""
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "step",
        "vehicle_id",
        "x",
        "y",
        "speed",
        "co2",
        "waiting_time"
    ])


    # ---- Simulation loop ----

    for step in range(NUM_STEPS):

        traci.simulationStep()


        # Get complete simulation state
        state = get_simulation_state(step)


        # ---- Vehicle data ----

        for vehicle in state.vehicles:

            writer.writerow([
                step,
                vehicle.id,
                vehicle.x,
                vehicle.y,
                vehicle.speed,
                vehicle.co2,
                vehicle.waiting_time
            ])


        # ---- Print state every 50 steps ----

        if step % 50 == 0:

            print(
                f"Step {step} | "
                f"Vehicles: {len(state.vehicles)} | "
                f"CO2: {state.total_co2:.2f} | "
                f"Waiting: {state.total_waiting_time:.2f} | "
                f"Traffic Lights: {len(state.traffic_lights)}"
            )


# ---- Close SUMO ----

traci.close()

print(
    f"\nDone! Data saved to {OUTPUT_CSV}"
)