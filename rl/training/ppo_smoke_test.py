"""
Minimal PPO integration smoke test for EcoFlux-RL.

Purpose:
- Register EcoTwinEnv with RLlib.
- Build a PPO algorithm.
- Run one short training iteration.
- Verify that RLlib can interact with SUMO successfully.
"""

import ray
from ray.tune.registry import register_env
from ray.rllib.algorithms.ppo import PPOConfig

from rl.environment.sumo_env import EcoTwinEnv


ENV_NAME = "EcoFluxEnv-v0"


def env_creator(env_config):
    return EcoTwinEnv(
        max_steps=20
    )


def main():
    print("=" * 60)
    print("EcoFlux RL - PPO Integration Smoke Test")
    print("=" * 60)

    # Register environment with RLlib.
    register_env(ENV_NAME, env_creator)

    # Start Ray.
    ray.init(
        ignore_reinit_error=True,
        include_dashboard=False,
    )

    try:
        config = (
            PPOConfig()
            .environment(
                env=ENV_NAME,
            )
            .env_runners(
                num_env_runners=0,
            )
            .training(
                train_batch_size_per_learner=200,
                minibatch_size=50,
                num_epochs=2,
                lr=0.0003,
            )
            .framework("torch")
        )

        print("\nBuilding PPO algorithm...")

        algo = config.build()

        print("PPO algorithm built successfully.")
        print("\nRunning one training iteration...\n")

        result = algo.train()

        print("=" * 60)
        print("PPO TRAINING ITERATION COMPLETED")
        print("=" * 60)

        print("Episode reward mean:",
              result.get("env_runners", {}).get("episode_return_mean"))

        print("Episode length mean:",
              result.get("env_runners", {}).get("episode_len_mean"))

        print("Environment steps:",
              result.get("num_env_steps_sampled"))

        print("\nPPO smoke test PASSED.")

        algo.stop()

    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()