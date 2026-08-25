"""
EcoFlux RL - Improved PPO Training

Ray RLlib 2.58.0
Python 3.12

Purpose:
    Train a stronger PPO traffic-signal control policy.

Changes from baseline:
    - More PPO iterations
    - Lower learning rate
    - Better PPO exploration
    - Explicit gamma/lambda
    - Gradient clipping
    - Separate improved checkpoint directory
    - Detailed metrics logging
"""

import csv
import os

import ray

from ray.tune.registry import register_env

from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.callbacks.callbacks import RLlibCallback

from rl.environment.sumo_env import EcoTwinEnv


# ============================================================
# CONFIGURATION
# ============================================================

ENV_NAME = "EcoFluxEnv-v0"

# ------------------------------------------------------------
# IMPORTANT
# ------------------------------------------------------------

# Baseline was only 5 iterations.
#
# Start with 50.
#
# If results are still poor, increase to 100.
#
NUM_ITERATIONS = 50

MAX_STEPS = 100


# ============================================================
# OUTPUT DIRECTORIES
# ============================================================

RESULTS_DIR = os.path.abspath(
    os.path.join(
        "rl",
        "results"
    )
)


CHECKPOINT_DIR = os.path.abspath(
    os.path.join(
        "rl",
        "checkpoints",
        "improved_ppo"
    )
)


CSV_FILE = os.path.join(
    RESULTS_DIR,
    "improved_ppo_metrics.csv"
)


# ============================================================
# ENVIRONMENT
# ============================================================

def env_creator(env_config):
    """
    Create one EcoFlux SUMO environment.
    """

    return EcoTwinEnv(
        max_steps=MAX_STEPS
    )


# ============================================================
# METRICS CALLBACK
# ============================================================

class EcoFluxMetricsCallback(RLlibCallback):
    """
    Collect final SUMO metrics from completed episodes.

    Expected environment info:

        total_co2
        total_waiting_time
        vehicle_count
    """

    def on_episode_end(
        self,
        *,
        episode,
        metrics_logger,
        **kwargs
    ):

        try:

            infos = episode.get_infos()

            if not infos:
                return

            # ------------------------------------------------
            # RLlib may return information in different forms.
            # Handle the common single-agent cases safely.
            # ------------------------------------------------

            final_info = None

            if isinstance(infos, list):

                if len(infos) > 0:

                    final_info = infos[-1]

            elif isinstance(infos, dict):

                # Single-agent case
                if len(infos) > 0:

                    values = list(
                        infos.values()
                    )

                    final_info = values[-1]

            if not isinstance(
                final_info,
                dict
            ):

                return

            # ------------------------------------------------
            # CO2
            # ------------------------------------------------

            total_co2 = float(
                final_info.get(
                    "total_co2",
                    0.0
                )
            )

            # ------------------------------------------------
            # Waiting Time
            # ------------------------------------------------

            total_waiting_time = float(
                final_info.get(
                    "total_waiting_time",
                    0.0
                )
            )

            # ------------------------------------------------
            # Vehicle Count
            # ------------------------------------------------

            vehicle_count = float(
                final_info.get(
                    "vehicle_count",
                    0.0
                )
            )

            # ------------------------------------------------
            # Send metrics to RLlib
            # ------------------------------------------------

            metrics_logger.log_value(
                "total_co2",
                total_co2,
                reduce="mean"
            )

            metrics_logger.log_value(
                "total_waiting_time",
                total_waiting_time,
                reduce="mean"
            )

            metrics_logger.log_value(
                "vehicle_count",
                vehicle_count,
                reduce="mean"
            )

        except Exception as error:

            print(
                "Metrics callback warning:",
                error
            )


# ============================================================
# DIRECTORY
# ============================================================

def create_results_directory():

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    os.makedirs(
        CHECKPOINT_DIR,
        exist_ok=True
    )


# ============================================================
# CSV INITIALIZATION
# ============================================================

def initialize_csv():

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "iteration",
                "episode_reward_mean",
                "episode_length_mean",
                "total_co2",
                "total_waiting_time",
                "vehicle_count",
                "num_env_steps_sampled"
            ]
        )


# ============================================================
# SAVE METRICS
# ============================================================

def save_metrics(
    iteration,
    reward,
    episode_length,
    total_co2,
    total_waiting_time,
    vehicle_count,
    env_steps
):

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                iteration,
                reward,
                episode_length,
                total_co2,
                total_waiting_time,
                vehicle_count,
                env_steps
            ]
        )


# ============================================================
# SAFE METRIC
# ============================================================

def get_metric(
    dictionary,
    key,
    default=None
):

    value = dictionary.get(
        key,
        default
    )

    if value is None:

        return default

    return value


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print(
        "EcoFlux RL - IMPROVED PPO TRAINING"
    )
    print("=" * 70)

    print()
    print(
        "Configuration:"
    )

    print(
        f"Environment       : {ENV_NAME}"
    )

    print(
        f"Iterations        : {NUM_ITERATIONS}"
    )

    print(
        f"Max steps         : {MAX_STEPS}"
    )

    print(
        f"Checkpoint folder : {CHECKPOINT_DIR}"
    )

    print(
        f"Metrics CSV       : {CSV_FILE}"
    )

    # ========================================================
    # DIRECTORIES
    # ========================================================

    create_results_directory()

    initialize_csv()

    # ========================================================
    # ENVIRONMENT REGISTRATION
    # ========================================================

    print()
    print(
        "Registering EcoFlux environment..."
    )

    register_env(
        ENV_NAME,
        env_creator
    )

    print(
        "EcoFlux environment registered."
    )

    # ========================================================
    # START RAY
    # ========================================================

    print()
    print(
        "Starting Ray..."
    )

    ray.init(
        ignore_reinit_error=True,
        include_dashboard=False
    )

    print(
        "Ray started."
    )

    algo = None

    try:

        # ====================================================
        # PPO CONFIGURATION
        # ====================================================

        print()
        print(
            "Building PPO configuration..."
        )

        config = (

            PPOConfig()

            # ------------------------------------------------
            # Environment
            # ------------------------------------------------

            .environment(
                env=ENV_NAME
            )

            # ------------------------------------------------
            # Environment runners
            # ------------------------------------------------

            .env_runners(
                num_env_runners=0
            )

            # ------------------------------------------------
            # PPO training
            # ------------------------------------------------

            .training(

                # Number of samples collected before
                # each learner update.

                train_batch_size_per_learner=1000,

                # Minibatch used for SGD.

                minibatch_size=128,

                # Number of passes over each batch.

                num_epochs=10,

                # Lower learning rate than baseline.

                lr=0.0001,

                # PPO clipping.

                clip_param=0.20,

                # Discount factor.

                gamma=0.99,

                # GAE lambda.

                lambda_=0.95,

                # Gradient clipping.

                grad_clip=0.5,

                # Entropy coefficient encourages
                # exploration.

                entropy_coeff=0.01
            )

            # ------------------------------------------------
            # Torch
            # ------------------------------------------------

            .framework(
                "torch"
            )

            # ------------------------------------------------
            # Callback
            # ------------------------------------------------

            .callbacks(
                EcoFluxMetricsCallback
            )
        )

        # ====================================================
        # BUILD ALGORITHM
        # ====================================================

        print()
        print(
            "Building PPO algorithm..."
        )

        algo = config.build()

        print()
        print(
            "PPO algorithm ready."
        )

        # ====================================================
        # TRAINING
        # ====================================================

        print()
        print("=" * 70)

        print(
            "STARTING IMPROVED PPO TRAINING"
        )

        print("=" * 70)

        # ----------------------------------------------------
        # Best metrics tracking
        # ----------------------------------------------------

        best_reward = None
        best_co2 = None
        best_waiting = None

        # ----------------------------------------------------
        # Training loop
        # ----------------------------------------------------

        for iteration in range(
            1,
            NUM_ITERATIONS + 1
        ):

            print()
            print(
                "=" * 70
            )

            print(
                f"PPO TRAINING ITERATION "
                f"{iteration}/{NUM_ITERATIONS}"
            )

            print(
                "=" * 70
            )

            # ------------------------------------------------
            # Train
            # ------------------------------------------------

            result = algo.train()

            # ------------------------------------------------
            # RLlib env metrics
            # ------------------------------------------------

            env_results = result.get(
                "env_runners",
                {}
            )

            # ------------------------------------------------
            # Reward
            # ------------------------------------------------

            reward = get_metric(
                env_results,
                "episode_return_mean"
            )

            # ------------------------------------------------
            # Episode length
            # ------------------------------------------------

            episode_length = get_metric(
                env_results,
                "episode_len_mean"
            )

            # ------------------------------------------------
            # CO2
            # ------------------------------------------------

            total_co2 = get_metric(
                env_results,
                "total_co2"
            )

            # ------------------------------------------------
            # Waiting
            # ------------------------------------------------

            total_waiting_time = get_metric(
                env_results,
                "total_waiting_time"
            )

            # ------------------------------------------------
            # Vehicle count
            # ------------------------------------------------

            vehicle_count = get_metric(
                env_results,
                "vehicle_count"
            )

            # ------------------------------------------------
            # Environment steps
            # ------------------------------------------------

            env_steps = result.get(
                "num_env_steps_sampled"
            )

            # ------------------------------------------------
            # PRINT
            # ------------------------------------------------

            print()

            print(
                f"Iteration          : "
                f"{iteration}"
            )

            print(
                f"Reward Mean        : "
                f"{reward}"
            )

            print(
                f"Episode Length     : "
                f"{episode_length}"
            )

            print(
                f"CO2                : "
                f"{total_co2}"
            )

            print(
                f"Waiting Time       : "
                f"{total_waiting_time}"
            )

            print(
                f"Vehicle Count      : "
                f"{vehicle_count}"
            )

            print(
                f"Environment Steps  : "
                f"{env_steps}"
            )

            # ------------------------------------------------
            # Track best reward
            # ------------------------------------------------

            if reward is not None:

                if (
                    best_reward is None
                    or reward > best_reward
                ):

                    best_reward = reward

            # ------------------------------------------------
            # Track best CO2
            # ------------------------------------------------

            if total_co2 is not None:

                if (
                    best_co2 is None
                    or total_co2 < best_co2
                ):

                    best_co2 = total_co2

            # ------------------------------------------------
            # Track best waiting
            # ------------------------------------------------

            if total_waiting_time is not None:

                if (
                    best_waiting is None
                    or total_waiting_time
                    < best_waiting
                ):

                    best_waiting = (
                        total_waiting_time
                    )

            # ------------------------------------------------
            # SAVE CSV
            # ------------------------------------------------

            save_metrics(
                iteration=iteration,
                reward=reward,
                episode_length=episode_length,
                total_co2=total_co2,
                total_waiting_time=(
                    total_waiting_time
                ),
                vehicle_count=vehicle_count,
                env_steps=env_steps
            )

            # ------------------------------------------------
            # Progress summary
            # ------------------------------------------------

            print()
            print(
                "-" * 70
            )

            print(
                f"Best Reward So Far : "
                f"{best_reward}"
            )

            print(
                f"Best CO2 So Far    : "
                f"{best_co2}"
            )

            print(
                f"Best Waiting So Far: "
                f"{best_waiting}"
            )

            print(
                "-" * 70
            )

        # ====================================================
        # SAVE CHECKPOINT
        # ====================================================

        print()
        print("=" * 70)

        print(
            "SAVING IMPROVED PPO CHECKPOINT"
        )

        print("=" * 70)

        checkpoint = algo.save_to_path(
            CHECKPOINT_DIR
        )

        print()
        print(
            "Checkpoint saved:"
        )

        print(
            checkpoint
        )

        # ====================================================
        # FINAL SUMMARY
        # ====================================================

        print()
        print("=" * 70)

        print(
            "IMPROVED PPO TRAINING COMPLETED"
        )

        print("=" * 70)

        print()
        print(
            f"Iterations completed : "
            f"{NUM_ITERATIONS}"
        )

        print(
            f"Best reward          : "
            f"{best_reward}"
        )

        print(
            f"Best CO2             : "
            f"{best_co2}"
        )

        print(
            f"Best waiting time    : "
            f"{best_waiting}"
        )

        print()
        print(
            "Checkpoint:"
        )

        print(
            checkpoint
        )

        print()
        print(
            "Metrics CSV:"
        )

        print(
            CSV_FILE
        )

        print()
        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)

        print(
            "IMPROVED PPO TRAINING FAILED"
        )

        print("=" * 70)

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        print("=" * 70)

        raise

    finally:

        # ----------------------------------------------------
        # Stop algorithm
        # ----------------------------------------------------

        if algo is not None:

            try:

                algo.stop()

            except Exception:
                pass

        # ----------------------------------------------------
        # Shutdown Ray
        # ----------------------------------------------------

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