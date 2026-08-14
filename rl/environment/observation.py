import numpy as np
from gymnasium import spaces


NUM_TRAFFIC_LIGHTS = 21
OBSERVATION_SIZE = 24


def create_observation_space():
    """
    Create the observation space for the EcoFlux RL agent.

    Observation contains:
        1. Vehicle count
        2. Total CO2 emission
        3. Total waiting time
        4. Traffic-light phases (21 values)

    Total = 24 values.
    """

    return spaces.Box(
        low=0.0,
        high=np.inf,
        shape=(OBSERVATION_SIZE,),
        dtype=np.float32
    )


def build_observation(
    vehicle_count,
    total_co2,
    total_waiting_time,
    traffic_light_phases
):
    """
    Convert SUMO simulation state into an RL observation.

    Parameters
    ----------
    vehicle_count : int
        Number of active vehicles.

    total_co2 : float
        Total CO2 emission.

    total_waiting_time : float
        Total vehicle waiting time.

    traffic_light_phases : list
        Current phase of each traffic light.

    Returns
    -------
    np.ndarray
        24-dimensional float32 observation.
    """

    phases = [
        float(phase)
        for phase in traffic_light_phases[:NUM_TRAFFIC_LIGHTS]
    ]

    # Ensure exactly 21 traffic-light phase values.
    while len(phases) < NUM_TRAFFIC_LIGHTS:
        phases.append(0.0)

    observation = np.array(
        [
            float(vehicle_count),
            float(total_co2),
            float(total_waiting_time),
            *phases
        ],
        dtype=np.float32
    )

    return observation


def validate_observation(observation):
    """
    Validate that an observation matches the RL environment.

    Returns
    -------
    np.ndarray
        Validated float32 observation.
    """

    observation = np.asarray(
        observation,
        dtype=np.float32
    )

    if observation.shape != (OBSERVATION_SIZE,):
        raise ValueError(
            f"Expected observation shape "
            f"({OBSERVATION_SIZE},), "
            f"got {observation.shape}"
        )

    if not np.all(np.isfinite(observation)):
        raise ValueError(
            "Observation contains NaN or infinite values."
        )

    return observation