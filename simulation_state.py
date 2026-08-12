import traci

from state_schema import (
    SimulationState,
    VehicleState,
    TrafficLightState
)


def get_simulation_state(step=0):
    """
    Get complete SUMO simulation state.

    Used for:
    - API/WebSocket integration
    - Dashboard
    - Complete simulation logging
    """

    vehicles = []

    # Collect complete vehicle information
    for vehicle_id in traci.vehicle.getIDList():

        x, y = traci.vehicle.getPosition(vehicle_id)
        speed = traci.vehicle.getSpeed(vehicle_id)
        co2 = traci.vehicle.getCO2Emission(vehicle_id)
        waiting_time = traci.vehicle.getWaitingTime(vehicle_id)

        vehicle = VehicleState(
            id=vehicle_id,
            x=float(x),
            y=float(y),
            speed=float(speed),
            co2=float(co2),
            waiting_time=float(waiting_time)
        )

        vehicles.append(vehicle)

    # Collect traffic-light information
    traffic_lights = []

    for tls_id in traci.trafficlight.getIDList():

        phase = traci.trafficlight.getPhase(tls_id)
        state = traci.trafficlight.getRedYellowGreenState(
            tls_id
        )

        traffic_light = TrafficLightState(
            id=tls_id,
            phase=int(phase),
            state=state
        )

        traffic_lights.append(traffic_light)

    # Calculate total CO2
    total_co2 = sum(
        vehicle.co2
        for vehicle in vehicles
    )

    # Calculate total waiting time
    total_waiting_time = sum(
        vehicle.waiting_time
        for vehicle in vehicles
    )

    # Return standardized simulation state
    return SimulationState(
        step=int(step),
        vehicles=vehicles,
        total_co2=float(total_co2),
        total_waiting_time=float(total_waiting_time),
        traffic_lights=traffic_lights
    )


def get_rl_observation():
    """
    Lightweight state collection for RL training.

    Only collects metrics required by the RL environment:
    - vehicle count
    - total CO2
    - total waiting time
    - traffic-light phases

    This avoids collecting unnecessary vehicle
    position and speed data during RL training.
    """

    vehicle_ids = traci.vehicle.getIDList()

    vehicle_count = len(vehicle_ids)

    total_co2 = 0.0
    total_waiting_time = 0.0

    # Collect only CO2 and waiting time
    for vehicle_id in vehicle_ids:

        total_co2 += traci.vehicle.getCO2Emission(
            vehicle_id
        )

        total_waiting_time += traci.vehicle.getWaitingTime(
            vehicle_id
        )

    # Collect traffic-light phases
    traffic_light_phases = []

    for tls_id in traci.trafficlight.getIDList():

        traffic_light_phases.append(
            traci.trafficlight.getPhase(tls_id)
        )

    return {
        "vehicle_count": vehicle_count,
        "total_co2": float(total_co2),
        "total_waiting_time": float(total_waiting_time),
        "traffic_light_phases": traffic_light_phases
    }