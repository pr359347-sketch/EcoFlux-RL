import traci

from api_interface import (
    get_current_state,
    get_current_state_json,
    get_state_summary
)


traci.start([
    "sumo",
    "-c",
    "citygrid.sumocfg"
])

traci.simulationStep()


print("API interface test started!")


state = get_current_state(step=1)

print("\nPython dictionary:")
print("Step:", state["step"])
print("Vehicles:", len(state["vehicles"]))
print("CO2:", state["total_co2"])
print("Waiting time:", state["total_waiting_time"])
print("Traffic lights:", len(state["traffic_lights"]))


summary = get_state_summary(step=1)

print("\nState summary:")
print(summary)


json_state = get_current_state_json(step=1)

print("\nJSON state:")
print(json_state[:500] + "...")


traci.close()

print("\nAPI interface test completed!")