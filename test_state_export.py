import traci

from state_export import get_state_json


traci.start([
    "sumo",
    "-c",
    "citygrid.sumocfg"
])

traci.simulationStep()

state = get_state_json(step=1)

print("API state export successful!")

print("\nStep:")
print(state["step"])

print("\nVehicles:")
print(len(state["vehicles"]))

print("\nTotal CO2:")
print(state["total_co2"])

print("\nTotal waiting time:")
print(state["total_waiting_time"])

print("\nTraffic lights:")
print(len(state["traffic_lights"]))

traci.close()

print("\nState export test completed!")