import json

from state_export import (
    get_state_json,
    get_state_json_string
)


def get_current_state(step=0):
    """
    Return the current simulation state as a Python dictionary.

    This function can be called by FastAPI/WebSocket code.
    """

    return get_state_json(step)


def get_current_state_json(step=0):
    """
    Return the current simulation state as a JSON string.

    Useful for WebSocket messages.
    """

    return get_state_json_string(step)


def get_state_summary(step=0):
    """
    Return a lightweight summary for dashboard/API use.
    """

    state = get_state_json(step)

    return {
        "step": state["step"],
        "vehicle_count": len(state["vehicles"]),
        "total_co2": state["total_co2"],
        "total_waiting_time": state["total_waiting_time"],
        "traffic_light_count": len(state["traffic_lights"])
    }


def state_to_json(data):
    """
    Convert a Python dictionary into a JSON string.
    """

    return json.dumps(data)