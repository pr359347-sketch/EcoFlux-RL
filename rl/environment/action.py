import numpy as np
from gymnasium import spaces


# EcoFlux contains 21 traffic-light junctions.
NUM_TRAFFIC_LIGHTS = 21

# First 9 traffic lights have 4 phases.
# Remaining 12 traffic lights have 3 phases.
PHASE_COUNTS = [4] * 9 + [3] * 12


def create_action_space():
    """
    Create the action space for the EcoFlux RL agent.

    Each traffic light receives one discrete phase index.
    """
    return spaces.MultiDiscrete(PHASE_COUNTS)


def validate_action(action):
    """
    Validate an RL action before sending it to SUMO.

    Parameters
    ----------
    action : array-like
        21 phase values, one for each traffic light.

    Returns
    -------
    np.ndarray
        Validated integer action.
    """

    action = np.asarray(action, dtype=np.int64)

    if action.shape != (NUM_TRAFFIC_LIGHTS,):
        raise ValueError(
            f"Expected {NUM_TRAFFIC_LIGHTS} actions, "
            f"got shape {action.shape}"
        )

    for index, phase in enumerate(action):
        if phase < 0 or phase >= PHASE_COUNTS[index]:
            raise ValueError(
                f"Invalid phase {phase} for traffic light {index}. "
                f"Expected range: "
                f"0 to {PHASE_COUNTS[index] - 1}"
            )

    return action


def sample_action():
    """
    Generate a random valid action.

    Useful for smoke testing before PPO training.
    """
    action_space = create_action_space()
    return action_space.sample()