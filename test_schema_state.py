import traci
from simulation_state import get_simulation_state

traci.start(["sumo", "-c", "citygrid.sumocfg"])

traci.simulationStep()

state = get_simulation_state(step=1)

print("State schema test successful!")
print("Step:", state.step)
print("Vehicles:", len(state.vehicles))
print("Total CO2:", state.total_co2)
print("Total waiting time:", state.total_waiting_time)
print("Traffic lights:", len(state.traffic_lights))

print("\nFirst vehicle:")

if state.vehicles:
    print(state.vehicles[0])

print("\nFirst traffic light:")

if state.traffic_lights:
    print(state.traffic_lights[0])

print("\nDictionary format:")
print(state.to_dict())

traci.close()

print("\nTest completed!")