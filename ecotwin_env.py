import traci
import gymnasium as gym
from gymnasium import spaces
import numpy as np

from simulation_state import get_rl_observation


class EcoTwinEnv(gym.Env):
    """
    SUMO-based Gymnasium environment for EcoTwin.
    """

    metadata = {"render_modes": []}

    def __init__(
        self,
        sumo_cfg="citygrid.sumocfg",
        max_steps=1000
    ):
        super().__init__()

        self.sumo_cfg = sumo_cfg
        self.max_steps = max_steps
        self.step_count = 0
        self.tls_ids = []

        # Actual SUMO phase counts:
        # A0-A2, B0-B2, C0-C2 -> 4 phases each
        # bottom, left, right, top -> 3 phases each
        self.phase_counts = (
            [4] * 9 +
            [3] * 12
        )

        # One discrete action for each of 21 traffic lights
        self.action_space = spaces.MultiDiscrete(
            self.phase_counts
        )

        # Observation:
        # vehicle count
        # total CO2
        # total waiting time
        # 21 traffic-light phases
        self.observation_space = spaces.Box(
            low=0.0,
            high=np.inf,
            shape=(24,),
            dtype=np.float32
        )

    def _start_sumo(self):
        """Start SUMO in headless mode."""

        if traci.isLoaded():
            traci.close()

        traci.start([
            "sumo",
            "-c",
            self.sumo_cfg
        ])

        self.tls_ids = list(
            traci.trafficlight.getIDList()
        )

    def _get_observation(self):
        """Get lightweight state for RL."""

        data = get_rl_observation()

        vehicle_count = data["vehicle_count"]
        total_co2 = data["total_co2"]
        total_waiting = data["total_waiting_time"]

        phases = [
            float(phase)
            for phase in data["traffic_light_phases"][:21]
        ]

        while len(phases) < 21:
            phases.append(0.0)

        observation = np.array(
            [
                float(vehicle_count),
                float(total_co2),
                float(total_waiting),
                *phases
            ],
            dtype=np.float32
        )

        return observation, data

    def reset(self, *, seed=None, options=None):
        """Reset SUMO environment."""

        super().reset(seed=seed)

        if traci.isLoaded():
            traci.close()

        self.step_count = 0

        self._start_sumo()

        traci.simulationStep()

        observation, data = self._get_observation()

        info = {
            "total_co2": data["total_co2"],
            "total_waiting_time": data["total_waiting_time"],
            "traffic_light_phases": data[
                "traffic_light_phases"
            ]
        }

        return observation, info

    def step(self, action):
        """Apply RL action and advance SUMO."""

        action = np.asarray(
            action,
            dtype=np.int64
        )

        # Make sure action has 21 values
        if len(action) != len(self.tls_ids):
            raise ValueError(
                f"Expected {len(self.tls_ids)} actions, "
                f"got {len(action)}"
            )

        # Apply phase actions
        for i, tls_id in enumerate(self.tls_ids):

            max_phase = self.phase_counts[i] - 1

            phase = int(
                np.clip(
                    action[i],
                    0,
                    max_phase
                )
            )

            traci.trafficlight.setPhase(
                tls_id,
                phase
            )

        # Advance SUMO
        traci.simulationStep()

        self.step_count += 1

        observation, data = self._get_observation()

        # Baseline reward
        reward = -(
            0.001 * data["total_co2"]
            + 0.01 * data["total_waiting_time"]
        )

        terminated = (
            traci.simulation.getMinExpectedNumber() <= 0
        )

        truncated = (
            self.step_count >= self.max_steps
        )

        info = {
            "total_co2": data["total_co2"],
            "total_waiting_time": data[
                "total_waiting_time"
            ],
            "traffic_light_phases": data[
                "traffic_light_phases"
            ]
        }

        return (
            observation,
            float(reward),
            terminated,
            truncated,
            info
        )

    def close(self):
        """Close SUMO safely."""

        if traci.isLoaded():
            traci.close()
