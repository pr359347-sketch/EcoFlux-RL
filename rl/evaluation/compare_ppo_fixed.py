"""
EcoFlux RL
PPO vs Fixed Timer Evaluation

Member-2 Evaluation

Compares:
    1. PPO Agent
    2. Fixed Timer Baseline

Metrics:
    - CO2
    - Waiting Time
    - Vehicle Count
    - Steps
"""

from __future__ import annotations

import csv
import os
import statistics

import numpy as np
import torch
import gymnasium as gym

import ray

from ray.rllib.algorithms.algorithm import Algorithm
from ray.rllib.core.columns import Columns
from ray.tune.registry import register_env

from rl.environment.sumo_env import EcoTwinEnv


# ============================================================
# CONFIGURATION
# ============================================================

MAX_STEPS = 100

NUM_EPISODES = 5

PHASE_DURATION = 10


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)


CHECKPOINT_PATH = os.path.join(
    PROJECT_ROOT,
    "rl",
    "checkpoints",
    "improved_ppo",
)


RESULTS_DIR = os.path.join(
    PROJECT_ROOT,
    "rl",
    "results",
)


RESULTS_FILE = os.path.join(
    RESULTS_DIR,
    "ppo_vs_fixed_comparison.csv",
)


# ============================================================
# ENVIRONMENT CREATOR
# ============================================================

def create_ecoflux_env(env_config=None):
    """
    Create EcoFlux SUMO environment.

    RLlib calls this function when creating
    an environment worker.
    """

    return EcoTwinEnv(
        max_steps=MAX_STEPS
    )


# ============================================================
# ENVIRONMENT REGISTRATION
# ============================================================

def register_ecoflux_environment():
    """
    Register EcoFlux environment with Gymnasium
    and RLlib.

    IMPORTANT:

    The PPO checkpoint contains:

        EcoFluxEnv

    Gymnasium expects a versioned environment:

        EcoFluxEnv-v0

    Therefore both registrations are handled.
    """

    print()
    print("=" * 70)
    print("REGISTERING ECOFLUX ENVIRONMENT")
    print("=" * 70)

    # --------------------------------------------------------
    # Gymnasium versioned environment
    # --------------------------------------------------------

    gym_env_id = "EcoFluxEnv-v0"

    try:

        gym.spec(gym_env_id)

        print(
            f"Gymnasium environment already exists: "
            f"{gym_env_id}"
        )

    except gym.error.Error:

        gym.register(
            id=gym_env_id,
            entry_point=create_ecoflux_env,
            disable_env_checker=True,
        )

        print(
            f"Gymnasium environment registered: "
            f"{gym_env_id}"
        )

    # --------------------------------------------------------
    # RLlib environment
    # --------------------------------------------------------

    register_env(
        "EcoFluxEnv",
        create_ecoflux_env,
    )

    print(
        "RLlib environment registered: EcoFluxEnv"
    )

    print(
        "Environment registration completed."
    )


# ============================================================
# METRIC EXTRACTION
# ============================================================

def extract_metrics(info):
    """
    Extract metrics returned by EcoTwinEnv.
    """

    if info is None:
        info = {}

    total_co2 = float(
        info.get(
            "total_co2",
            0.0,
        )
    )

    total_waiting_time = float(
        info.get(
            "total_waiting_time",
            0.0,
        )
    )

    vehicle_count = int(
        info.get(
            "vehicle_count",
            0,
        )
    )

    return {
        "total_co2": total_co2,
        "total_waiting_time": total_waiting_time,
        "vehicle_count": vehicle_count,
    }


# ============================================================
# AVERAGE METRICS
# ============================================================

def calculate_average(results):
    """
    Calculate average metrics across episodes.
    """

    if not results:

        return {
            "total_co2": 0.0,
            "total_waiting_time": 0.0,
            "vehicle_count": 0.0,
        }

    return {
        "total_co2": statistics.mean(
            result["total_co2"]
            for result in results
        ),

        "total_waiting_time": statistics.mean(
            result["total_waiting_time"]
            for result in results
        ),

        "vehicle_count": statistics.mean(
            result["vehicle_count"]
            for result in results
        ),
    }


# ============================================================
# PERCENTAGE REDUCTION
# ============================================================

def calculate_reduction(
    baseline,
    new_value,
):
    """
    Calculate percentage reduction.

    Positive value means PPO improved
    compared with baseline.
    """

    if baseline == 0:

        return 0.0

    return (
        (baseline - new_value)
        / baseline
    ) * 100.0


# ============================================================
# FIXED TIMER EPISODE
# ============================================================

def run_fixed_timer_episode(
    episode_number,
):
    """
    Run one fixed-timer episode.
    """

    print()
    print("-" * 70)

    print(
        f"FIXED TIMER EPISODE "
        f"{episode_number}/{NUM_EPISODES}"
    )

    print("-" * 70)

    env = EcoTwinEnv(
        max_steps=MAX_STEPS
    )

    try:

        observation, info = env.reset(
            seed=episode_number
        )

        final_info = info

        # ----------------------------------------------------
        # Action-space phase counts
        # ----------------------------------------------------

        phase_counts = [
            int(value)
            for value in env.action_space.nvec
        ]

        # ----------------------------------------------------
        # Initial phase for each traffic light
        # ----------------------------------------------------

        current_phases = [
            0
            for _ in phase_counts
        ]

        # ----------------------------------------------------
        # Run episode
        # ----------------------------------------------------

        for step in range(
            MAX_STEPS
        ):

            action = np.asarray(
                current_phases,
                dtype=np.int64,
            )

            (
                observation,
                reward,
                terminated,
                truncated,
                info,
            ) = env.step(
                action
            )

            final_info = info

            # ------------------------------------------------
            # Fixed timer phase change
            # ------------------------------------------------

            if (
                (step + 1)
                % PHASE_DURATION
                == 0
            ):

                for index in range(
                    len(current_phases)
                ):

                    current_phases[index] = (
                        current_phases[index] + 1
                    ) % phase_counts[index]

            # ------------------------------------------------
            # Print progress
            # ------------------------------------------------

            if (
                (step + 1) % 10 == 0
            ):

                metrics = extract_metrics(
                    final_info
                )

                print(
                    f"Step {step + 1:03d} | "
                    f"CO2: "
                    f"{metrics['total_co2']:.2f} | "
                    f"Waiting: "
                    f"{metrics['total_waiting_time']:.2f} | "
                    f"Vehicles: "
                    f"{metrics['vehicle_count']}"
                )

            if (
                terminated
                or truncated
            ):

                break

        # ----------------------------------------------------
        # Final metrics
        # ----------------------------------------------------

        result = extract_metrics(
            final_info
        )

        print()
        print(
            "Fixed Timer Episode Completed"
        )

        print(
            f"CO2          : "
            f"{result['total_co2']:.2f}"
        )

        print(
            f"Waiting Time : "
            f"{result['total_waiting_time']:.2f}"
        )

        print(
            f"Vehicle Count: "
            f"{result['vehicle_count']}"
        )

        return result

    finally:

        env.close()


# ============================================================
# PPO ACTION
# ============================================================

def get_ppo_action(
    module,
    observation,
):
    """
    Generate deterministic PPO action.

    EcoFlux action space:

        9 traffic lights  -> 4 phases
        12 traffic lights -> 3 phases

    Total:

        9 * 4  = 36
        12 * 3 = 36

        Total logits = 72

    Final action:

        21 phase values
    """

    # --------------------------------------------------------
    # Convert observation
    # --------------------------------------------------------

    observation_array = np.asarray(
        observation,
        dtype=np.float32,
    )

    observation_tensor = torch.as_tensor(
        observation_array,
        dtype=torch.float32,
    )

    # --------------------------------------------------------
    # Add batch dimension
    # --------------------------------------------------------

    if observation_tensor.ndim == 1:

        observation_tensor = (
            observation_tensor.unsqueeze(0)
        )

    # --------------------------------------------------------
    # RLlib inference batch
    # --------------------------------------------------------

    batch = {
        Columns.OBS: observation_tensor
    }

    # --------------------------------------------------------
    # Run RLModule
    # --------------------------------------------------------

    output = module.forward_inference(
        batch
    )

    # --------------------------------------------------------
    # If RLlib directly returned actions
    # --------------------------------------------------------

    if Columns.ACTIONS in output:

        action = output[
            Columns.ACTIONS
        ]

        if isinstance(
            action,
            torch.Tensor,
        ):

            action = (
                action
                .detach()
                .cpu()
                .numpy()
            )

        action = np.asarray(
            action,
            dtype=np.int64,
        )

        if (
            action.ndim > 1
            and action.shape[0] == 1
        ):

            action = action[0]

        return action.reshape(21)

    # --------------------------------------------------------
    # Otherwise get action distribution logits
    # --------------------------------------------------------

    if (
        Columns.ACTION_DIST_INPUTS
        in output
    ):

        logits = output[
            Columns.ACTION_DIST_INPUTS
        ]

    elif (
        "action_dist_inputs"
        in output
    ):

        logits = output[
            "action_dist_inputs"
        ]

    else:

        raise RuntimeError(
            "\nPPO RLModule did not return "
            "actions or action distribution inputs.\n\n"
            f"Available keys: "
            f"{list(output.keys())}"
        )

    # --------------------------------------------------------
    # Torch -> NumPy
    # --------------------------------------------------------

    if isinstance(
        logits,
        torch.Tensor,
    ):

        logits = (
            logits
            .detach()
            .cpu()
            .numpy()
        )

    logits = np.asarray(
        logits,
        dtype=np.float32,
    )

    # --------------------------------------------------------
    # Remove batch dimension
    # --------------------------------------------------------

    if (
        logits.ndim > 1
        and logits.shape[0] == 1
    ):

        logits = logits[0]

    # --------------------------------------------------------
    # EcoFlux action structure
    # --------------------------------------------------------

    phase_counts = (
        [4] * 9
        + [3] * 12
    )

    expected_logits = sum(
        phase_counts
    )

    # --------------------------------------------------------
    # Validate logits
    # --------------------------------------------------------

    if logits.size != expected_logits:

        raise ValueError(
            "\nUnexpected PPO logits size.\n"
            f"Expected: {expected_logits}\n"
            f"Received: {logits.size}\n"
            f"Shape: {logits.shape}"
        )

    # --------------------------------------------------------
    # Convert 72 logits -> 21 actions
    # --------------------------------------------------------

    actions = []

    position = 0

    for phase_count in phase_counts:

        phase_logits = logits[
            position:
            position + phase_count
        ]

        # ----------------------------------------------------
        # Deterministic action
        # ----------------------------------------------------

        selected_phase = int(
            np.argmax(
                phase_logits
            )
        )

        actions.append(
            selected_phase
        )

        position += phase_count

    action = np.asarray(
        actions,
        dtype=np.int64,
    )

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    if action.shape != (21,):

        raise ValueError(
            "\nInvalid PPO action shape.\n"
            f"Expected: (21,)\n"
            f"Received: {action.shape}"
        )

    return action


# ============================================================
# PPO EPISODE
# ============================================================

def run_ppo_episode(
    algo,
    episode_number,
):
    """
    Run one PPO evaluation episode.
    """

    print()
    print("-" * 70)

    print(
        f"PPO EPISODE "
        f"{episode_number}/{NUM_EPISODES}"
    )

    print("-" * 70)

    env = EcoTwinEnv(
        max_steps=MAX_STEPS
    )

    try:

        observation, info = env.reset(
            seed=episode_number
        )

        final_info = info

        # ----------------------------------------------------
        # Get RLModule
        # ----------------------------------------------------

        module = algo.get_module()

        if module is None:

            raise RuntimeError(
                "PPO RLModule could not be loaded."
            )

        print(
            "PPO RLModule loaded successfully."
        )

        # ----------------------------------------------------
        # Run episode
        # ----------------------------------------------------

        for step in range(
            MAX_STEPS
        ):

            action = get_ppo_action(
                module,
                observation,
            )

            # ------------------------------------------------
            # Validate action count
            # ------------------------------------------------

            expected_size = len(
                env.action_space.nvec
            )

            if action.size != expected_size:

                raise ValueError(
                    "\nInvalid PPO action size.\n"
                    f"Expected: {expected_size}\n"
                    f"Received: {action.size}"
                )

            # ------------------------------------------------
            # Validate each phase
            # ------------------------------------------------

            for index, value in enumerate(
                action
            ):

                max_value = (
                    int(
                        env.action_space.nvec[
                            index
                        ]
                    )
                    - 1
                )

                if (
                    value < 0
                    or value > max_value
                ):

                    raise ValueError(
                        "\nInvalid PPO action.\n"
                        f"Traffic Light: {index}\n"
                        f"Action: {value}\n"
                        f"Valid range: "
                        f"0-{max_value}"
                    )

            # ------------------------------------------------
            # Step environment
            # ------------------------------------------------

            (
                observation,
                reward,
                terminated,
                truncated,
                info,
            ) = env.step(
                action
            )

            final_info = info

            # ------------------------------------------------
            # Progress
            # ------------------------------------------------

            if (
                (step + 1) % 10 == 0
            ):

                metrics = extract_metrics(
                    final_info
                )

                print(
                    f"Step {step + 1:03d} | "
                    f"Reward: {reward:.4f} | "
                    f"CO2: "
                    f"{metrics['total_co2']:.2f} | "
                    f"Waiting: "
                    f"{metrics['total_waiting_time']:.2f} | "
                    f"Vehicles: "
                    f"{metrics['vehicle_count']}"
                )

            if (
                terminated
                or truncated
            ):

                break

        # ----------------------------------------------------
        # Final metrics
        # ----------------------------------------------------

        result = extract_metrics(
            final_info
        )

        print()
        print(
            "PPO Episode Completed"
        )

        print(
            f"CO2          : "
            f"{result['total_co2']:.2f}"
        )

        print(
            f"Waiting Time : "
            f"{result['total_waiting_time']:.2f}"
        )

        print(
            f"Vehicle Count: "
            f"{result['vehicle_count']}"
        )

        return result

    finally:

        env.close()


# ============================================================
# SAVE COMPARISON
# ============================================================

def save_comparison(
    fixed_average,
    ppo_average,
):
    """
    Save PPO vs Fixed Timer comparison.
    """

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Improvements
    # --------------------------------------------------------

    co2_reduction = calculate_reduction(
        fixed_average["total_co2"],
        ppo_average["total_co2"],
    )

    waiting_reduction = calculate_reduction(
        fixed_average["total_waiting_time"],
        ppo_average["total_waiting_time"],
    )

    vehicle_difference = (
        ppo_average["vehicle_count"]
        - fixed_average["vehicle_count"]
    )

    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    with open(
        RESULTS_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "metric",
                "fixed_timer",
                "ppo",
                "improvement_percent",
            ]
        )

        writer.writerow(
            [
                "total_co2",
                fixed_average[
                    "total_co2"
                ],
                ppo_average[
                    "total_co2"
                ],
                co2_reduction,
            ]
        )

        writer.writerow(
            [
                "total_waiting_time",
                fixed_average[
                    "total_waiting_time"
                ],
                ppo_average[
                    "total_waiting_time"
                ],
                waiting_reduction,
            ]
        )

        writer.writerow(
            [
                "vehicle_count",
                fixed_average[
                    "vehicle_count"
                ],
                ppo_average[
                    "vehicle_count"
                ],
                vehicle_difference,
            ]
        )

    print()
    print("=" * 70)

    print(
        "Comparison CSV saved:"
    )

    print(
        RESULTS_FILE
    )

    print("=" * 70)


# ============================================================
# FINAL COMPARISON
# ============================================================

def print_final_comparison(
    fixed_average,
    ppo_average,
):
    """
    Print final comparison.
    """

    co2_reduction = calculate_reduction(
        fixed_average["total_co2"],
        ppo_average["total_co2"],
    )

    waiting_reduction = calculate_reduction(
        fixed_average["total_waiting_time"],
        ppo_average["total_waiting_time"],
    )

    vehicle_difference = (
        ppo_average["vehicle_count"]
        - fixed_average["vehicle_count"]
    )

    print()
    print()
    print("=" * 70)

    print(
        "FINAL PPO vs FIXED-TIMER COMPARISON"
    )

    print("=" * 70)

    print()

    print(
        f"{'Metric':<25}"
        f"{'Fixed Timer':>18}"
        f"{'PPO':>18}"
    )

    print(
        "-" * 61
    )

    print(
        f"{'CO2':<25}"
        f"{fixed_average['total_co2']:>18.2f}"
        f"{ppo_average['total_co2']:>18.2f}"
    )

    print(
        f"{'Waiting Time':<25}"
        f"{fixed_average['total_waiting_time']:>18.2f}"
        f"{ppo_average['total_waiting_time']:>18.2f}"
    )

    print(
        f"{'Vehicle Count':<25}"
        f"{fixed_average['vehicle_count']:>18.2f}"
        f"{ppo_average['vehicle_count']:>18.2f}"
    )

    print()

    print(
        "-" * 61
    )

    print(
        f"CO2 Reduction     : "
        f"{co2_reduction:.2f}%"
    )

    print(
        f"Waiting Reduction : "
        f"{waiting_reduction:.2f}%"
    )

    print(
        f"Vehicle Difference: "
        f"{vehicle_difference:.2f}"
    )

    print()

    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)

    print(
        "EcoFlux RL - PPO vs Fixed Timer"
    )

    print("=" * 70)

    # ========================================================
    # CHECKPOINT CHECK
    # ========================================================

    print()
    print(
        "Checking PPO checkpoint..."
    )

    print(
        CHECKPOINT_PATH
    )

    if not os.path.exists(
        CHECKPOINT_PATH
    ):

        raise FileNotFoundError(
            "\nPPO checkpoint not found.\n\n"
            f"Expected:\n"
            f"{CHECKPOINT_PATH}\n"
        )

    print(
        "Checkpoint found."
    )

    # ========================================================
    # RAY INITIALIZATION
    # ========================================================

    print()
    print(
        "Starting Ray..."
    )

    ray.init(
        ignore_reinit_error=True,
        include_dashboard=False,
    )

    print(
        "Ray started."
    )

    algo = None

    try:

        # ====================================================
        # REGISTER ENVIRONMENT
        # ====================================================

        register_ecoflux_environment()

        # ====================================================
        # LOAD PPO CHECKPOINT
        # ====================================================

        print()
        print("=" * 70)

        print(
            "LOADING PPO CHECKPOINT"
        )

        print("=" * 70)

        print()
        print(
            "Loading checkpoint..."
        )

        algo = Algorithm.from_checkpoint(
            CHECKPOINT_PATH
        )

        print()
        print(
            "PPO checkpoint loaded successfully."
        )

        # ====================================================
        # FIXED TIMER EVALUATION
        # ====================================================

        print()
        print("=" * 70)

        print(
            "FIXED TIMER EVALUATION"
        )

        print("=" * 70)

        fixed_results = []

        for episode_number in range(
            1,
            NUM_EPISODES + 1,
        ):

            result = run_fixed_timer_episode(
                episode_number
            )

            fixed_results.append(
                result
            )

        # ====================================================
        # PPO EVALUATION
        # ====================================================

        print()
        print("=" * 70)

        print(
            "PPO EVALUATION"
        )

        print("=" * 70)

        ppo_results = []

        for episode_number in range(
            1,
            NUM_EPISODES + 1,
        ):

            result = run_ppo_episode(
                algo,
                episode_number
            )

            ppo_results.append(
                result
            )

        # ====================================================
        # AVERAGES
        # ====================================================

        print()
        print(
            "Calculating average metrics..."
        )

        fixed_average = calculate_average(
            fixed_results
        )

        ppo_average = calculate_average(
            ppo_results
        )

        # ====================================================
        # SAVE
        # ====================================================

        save_comparison(
            fixed_average,
            ppo_average,
        )

        # ====================================================
        # FINAL RESULT
        # ====================================================

        print_final_comparison(
            fixed_average,
            ppo_average,
        )

        print()
        print("=" * 70)

        print(
            "PPO vs Fixed Timer evaluation completed."
        )

        print("=" * 70)

    finally:

        # ====================================================
        # STOP ALGORITHM
        # ====================================================

        if algo is not None:

            try:

                algo.stop()

            except Exception:

                pass

        # ====================================================
        # SHUTDOWN RAY
        # ====================================================

        try:

            ray.shutdown()

        except Exception:

            pass

        print()
        print(
            "Ray shutdown completed."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
