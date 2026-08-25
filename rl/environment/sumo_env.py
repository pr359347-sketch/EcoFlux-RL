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

from rl.environment.reward import (
    calculate_reward,
)


class EcoTwinEnv(Env):
    """
    Gymnasium environment that controls SUMO traffic lights.

    The environment uses a step-based reward.

    Reward objectives:
        1. Reduce CO2.
        2. Reduce waiting time.
    """

    metadata = {
        "render_modes": []
    }

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

        # ----------------------------------------------------
        # Previous metrics used by the reward function.
        # ----------------------------------------------------

        self.previous_co2 = 0.0

        self.previous_waiting_time = 0.0

        # ----------------------------------------------------
        # Action / observation spaces.
        # ----------------------------------------------------

        self.action_space = create_action_space()

        self.observation_space = (
            create_observation_space()
        )

    # ========================================================
    # START SUMO
    # ========================================================

    def _start_sumo(self) -> None:
        """
        Start SUMO in headless mode.
        """

        if traci.isLoaded():

            traci.close()

        traci.start(
            [
                "sumo",
                "-c",
                self.sumo_cfg,
            ]
        )

        self.tls_ids = list(
            traci.trafficlight.getIDList()
        )

        expected_tls = (
            self.action_space.nvec.shape[0]
        )

        if len(self.tls_ids) != expected_tls:

            raise RuntimeError(
                f"SUMO exposes "
                f"{len(self.tls_ids)} traffic lights, "
                f"but the RL action space expects "
                f"{expected_tls}."
            )

    # ========================================================
    # OBSERVATION
    # ========================================================

    def _get_observation(self):
        """
        Collect current SUMO state for RL.
        """

        data = get_rl_observation()

        observation = build_observation(
            vehicle_count=data[
                "vehicle_count"
            ],

            total_co2=data[
                "total_co2"
            ],

            total_waiting_time=data[
                "total_waiting_time"
            ],

            traffic_light_phases=data[
                "traffic_light_phases"
            ],
        )

        return observation, data

    # ========================================================
    # INFO
    # ========================================================

    @staticmethod
    def _build_info(
        data: dict
    ) -> dict:
        """
        Build information returned to
        training and evaluation.
        """

        return {
            "total_co2": float(
                data["total_co2"]
            ),

            "total_waiting_time": float(
                data[
                    "total_waiting_time"
                ]
            ),

            "vehicle_count": int(
                data["vehicle_count"]
            ),

            "traffic_light_phases": list(
                data[
                    "traffic_light_phases"
                ]
            ),
        }

    # ========================================================
    # RESET
    # ========================================================

    def reset(
        self,
        *,
        seed=None,
        options=None
    ):
        """
        Reset SUMO and return initial observation.
        """

        super().reset(
            seed=seed
        )

        # ----------------------------------------------------
        # Close previous SUMO instance.
        # ----------------------------------------------------

        if traci.isLoaded():

            traci.close()

        # ----------------------------------------------------
        # Reset counters.
        # ----------------------------------------------------

        self.step_count = 0

        # ----------------------------------------------------
        # Reset previous reward metrics.
        # ----------------------------------------------------

        self.previous_co2 = 0.0

        self.previous_waiting_time = 0.0

        # ----------------------------------------------------
        # Start SUMO.
        # ----------------------------------------------------

        self._start_sumo()

        # ----------------------------------------------------
        # Advance simulation once to obtain
        # the initial state.
        # ----------------------------------------------------

        traci.simulationStep()

        # ----------------------------------------------------
        # Read initial state.
        # ----------------------------------------------------

        observation, data = (
            self._get_observation()
        )

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # The first reward comparison should start from
        # the actual initial SUMO values.
        # ----------------------------------------------------

        self.previous_co2 = float(
            data["total_co2"]
        )

        self.previous_waiting_time = float(
            data[
                "total_waiting_time"
            ]
        )

        return (
            observation,
            self._build_info(data)
        )

    # ========================================================
    # STEP
    # ========================================================

    def step(
        self,
        action
    ):
        """
        Apply traffic-light phases and
        advance SUMO by one step.
        """

        # ----------------------------------------------------
        # Validate action.
        # ----------------------------------------------------

        action = validate_action(
            action
        )

        # ----------------------------------------------------
        # Validate number of actions.
        # ----------------------------------------------------

        if len(action) != len(
            self.tls_ids
        ):

            raise ValueError(
                f"Expected "
                f"{len(self.tls_ids)} actions, "
                f"got {len(action)}."
            )

        # ====================================================
        # APPLY ACTION
        # ====================================================

        for i, tls_id in enumerate(
            self.tls_ids
        ):

            traci.trafficlight.setPhase(
                tls_id,
                int(action[i])
            )

        # ====================================================
        # ADVANCE SUMO
        # ====================================================

        traci.simulationStep()

        self.step_count += 1

        # ====================================================
        # GET NEW STATE
        # ====================================================

        observation, data = (
            self._get_observation()
        )

        # ====================================================
        # CURRENT METRICS
        # ====================================================

        current_co2 = float(
            data["total_co2"]
        )

        current_waiting_time = float(
            data[
                "total_waiting_time"
            ]
        )

        # ====================================================
        # CALCULATE STEP REWARD
        # ====================================================

        reward = calculate_reward(
            total_co2=current_co2,

            total_waiting_time=(
                current_waiting_time
            ),

            previous_co2=(
                self.previous_co2
            ),

            previous_waiting_time=(
                self.previous_waiting_time
            ),
        )

        # ====================================================
        # UPDATE PREVIOUS METRICS
        # ====================================================

        self.previous_co2 = (
            current_co2
        )

        self.previous_waiting_time = (
            current_waiting_time
        )

        # ====================================================
        # TERMINATION
        # ====================================================

        terminated = (
            traci.simulation
            .getMinExpectedNumber()
            <= 0
        )

        # ====================================================
        # TRUNCATION
        # ====================================================

        truncated = (
            self.step_count
            >= self.max_steps
        )

        # ====================================================
        # RETURN
        # ====================================================

        return (
            observation,

            float(reward),

            terminated,

            truncated,

            self._build_info(data),
        )

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self) -> None:
        """
        Close SUMO safely.
        """

        if traci.isLoaded():

            traci.close()


__all__ = [
    "EcoTwinEnv"
]