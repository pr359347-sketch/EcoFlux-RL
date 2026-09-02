import numpy as np


NUM_TRAFFIC_LIGHTS = 21
PHASE_COUNTS = [4] * 9 + [3] * 12


class RLService:
    """
    Backend RL service interface for EcoTwin.

    Compatible with the action-space contract defined by the
    RL component: 21 traffic lights with discrete phase actions.

    The trained PPO checkpoint can be connected later without
    changing the API endpoints.
    """

    def __init__(self):
        self.initialized = False
        self.last_action = None

    def initialize(self):
        self.initialized = True

        return {
            "status": "initialized",
            "message": "RL service initialized successfully",
            "action_space": {
                "type": "MultiDiscrete",
                "traffic_lights": NUM_TRAFFIC_LIGHTS,
                "phase_counts": PHASE_COUNTS,
            },
        }

    def get_action(self, state: dict):
        if not self.initialized:
            self.initialize()

        # Safe backend fallback until the trained PPO checkpoint
        # is available in the Member-3 runtime environment.
        action = np.zeros(
            NUM_TRAFFIC_LIGHTS,
            dtype=np.int64,
        )

        self.last_action = action.tolist()

        return {
            "action": self.last_action,
            "action_type": "phase_control",
            "traffic_lights": NUM_TRAFFIC_LIGHTS,
            "state": state,
        }

    def reset(self):
        self.initialized = False
        self.last_action = None

        return {
            "status": "reset",
            "message": "RL service reset successfully",
        }


rl_service = RLService()