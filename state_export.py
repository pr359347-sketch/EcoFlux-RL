import json

from simulation_state import get_simulation_state


def get_state_json(step=0):
    """
    Get the current SUMO simulation state
    in JSON format for API/WebSocket use.
    """

    state = get_simulation_state(step)

    return state.to_dict()


def get_state_json_string(step=0):
    """
    Return simulation state as a JSON string.
    """

    state = get_state_json(step)

    return json.dumps(state)