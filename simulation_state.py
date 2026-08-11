import traci


def get_simulation_state():
    """Return the current SUMO simulation state in a clean dictionary."""

    vehicles = []

    for vehicle_id in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(vehicle_id)

        vehicles.append({
            "id": vehicle_id,
            "x": x,
            "y": y,
            "speed": traci.vehicle.getSpeed(vehicle_id),
            "co2": traci.vehicle.getCO2Emission(vehicle_id),
            "waiting_time": traci.vehicle.getWaitingTime(vehicle_id)
        })

    traffic_lights = {}

    for tls_id in traci.trafficlight.getIDList():
        traffic_lights[tls_id] = {
            "phase": traci.trafficlight.getPhase(tls_id),
            "state": traci.trafficlight.getRedYellowGreenState(tls_id)
        }

    total_co2 = sum(v["co2"] for v in vehicles)

    total_waiting_time = sum(
        v["waiting_time"] for v in vehicles
    )

    return {
        "vehicles": vehicles,
        "total_co2": total_co2,
        "total_waiting_time": total_waiting_time,
        "traffic_lights": traffic_lights
    }