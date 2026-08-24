"""SUMO-backed Gymnasium environment for the EcoFlux RL agent."""

from __future__ import annotations

import traci
from gymnasium import Env

from simulation_state import get_rl_observation
from rl.environment.action import (
    create_action_space,
    validate_action,
)
from rl.environment.observation import (
    build_observation,
    create_observation_space,
)
from rl.environment.reward import calculate_reward


class EcoTwinEnv(Env):
    """Gymnasium environment that controls SUMO traffic lights."""

    metadata = {"render_modes": []}

    def __init__(
        self,
        sumo_cfg: str = "citygrid.sumocfg",
        max_steps: int = 1000,
    ) -> None:
        super().__init__()

        self.sumo_cfg = sumo_cfg
        self.max_steps = max_steps
        self.step_count = 0
        self.tls_ids: list[str] = []

        self.action_space = create_action_space()
        self.observation_space = create_observation_space()

    def _start_sumo(self) -> None:
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

        expected_tls = self.action_space.nvec.shape[0]

        if len(self.tls_ids) != expected_tls:
            raise RuntimeError(
                f"SUMO exposes {len(self.tls_ids)} traffic lights, "
                f"but the RL action space expects {expected_tls}."
            )

    def _get_observation(self):
        """Collect current SUMO state for RL."""

        data = get_rl_observation()

        observation = build_observation(
            vehicle_count=data["vehicle_count"],
            total_co2=data["total_co2"],
            total_waiting_time=data["total_waiting_time"],
            traffic_light_phases=data[
                "traffic_light_phases"
            ],
        )

        return observation, data

    @staticmethod
    def _build_info(data: dict) -> dict:
        """Build information returned to training/evaluation."""

        return {
            "total_co2": float(
                data["total_co2"]
            ),
            "total_waiting_time": float(
                data["total_waiting_time"]
            ),
            "vehicle_count": int(
                data["vehicle_count"]
            ),
            "traffic_light_phases": list(
                data["traffic_light_phases"]
            ),
        }

    def reset(self, *, seed=None, options=None):
        """Reset SUMO and return initial observation."""

        super().reset(seed=seed)

        if traci.isLoaded():
            traci.close()

        self.step_count = 0

        self._start_sumo()

        traci.simulationStep()

        observation, data = self._get_observation()

        return (
            observation,
            self._build_info(data)
        )

    def step(self, action):
        """Apply traffic-light phases and advance SUMO."""

        action = validate_action(action)

        if len(action) != len(self.tls_ids):
            raise ValueError(
                f"Expected {len(self.tls_ids)} actions, "
                f"got {len(action)}."
            )

        # Apply RL action to every traffic light
        for i, tls_id in enumerate(self.tls_ids):

            traci.trafficlight.setPhase(
                tls_id,
                int(action[i])
            )

        # Advance simulation
        traci.simulationStep()

        self.step_count += 1

        # Get new state
        observation, data = self._get_observation()

        # Centralized reward calculation
        reward = calculate_reward(
            total_co2=data["total_co2"],
            total_waiting_time=data[
                "total_waiting_time"
            ],
        )

        terminated = (
            traci.simulation.getMinExpectedNumber()
            <= 0
        )

        truncated = (
            self.step_count >= self.max_steps
        )

        return (
            observation,
            float(reward),
            terminated,
            truncated,
            self._build_info(data),
        )

    def close(self) -> None:
        """Close SUMO safely."""

        if traci.isLoaded():
            traci.close()


__all__ = ["EcoTwinEnv"]
