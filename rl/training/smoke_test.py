"""
Random-agent smoke test for the EcoFlux RL environment.

This test verifies that:
1. The environment can reset successfully.
2. Random valid actions can be generated.
3. Actions can be passed to SUMO.
4. Observations have the expected shape.
5. Rewards are returned correctly.
6. The environment can run multiple steps without crashing.
"""

from rl.environment.sumo_env import EcoTwinEnv
from rl.environment.action import sample_action


def run_smoke_test(num_steps: int = 20) -> None:
    """Run a short random-agent episode."""

    env = EcoTwinEnv(max_steps=num_steps)

    try:
        observation, info = env.reset()

        print("=" * 60)
        print("EcoFlux RL - Random Agent Smoke Test")
        print("=" * 60)

        print(f"Initial observation shape: {observation.shape}")
        print(f"Initial observation: {observation}")
        print(f"Initial info: {info}")
        print()

        expected_shape = env.observation_space.shape

        if observation.shape != expected_shape:
            raise AssertionError(
                f"Expected observation shape {expected_shape}, "
                f"got {observation.shape}"
            )

        total_reward = 0.0

        for step in range(1, num_steps + 1):

            # Generate a valid random action
            action = sample_action()

            # Apply action to environment
            (
                observation,
                reward,
                terminated,
                truncated,
                info,
            ) = env.step(action)

            total_reward += reward

            print(
                f"Step {step:02d} | "
                f"Reward: {reward:10.4f} | "
                f"CO2: {info['total_co2']:12.2f} | "
                f"Waiting: {info['total_waiting_time']:10.2f}"
            )

            # Validate observation
            if observation.shape != expected_shape:
                raise AssertionError(
                    f"Invalid observation shape at step {step}: "
                    f"{observation.shape}"
                )

            # Validate reward
            if not isinstance(reward, (int, float)):
                raise TypeError(
                    f"Reward must be numeric, got {type(reward)}"
                )

            if terminated or truncated:
                print()
                print(
                    f"Episode ended at step {step}. "
                    f"terminated={terminated}, "
                    f"truncated={truncated}"
                )
                break

        print()
        print("-" * 60)
        print(f"Total reward: {total_reward:.4f}")
        print("Random-agent smoke test PASSED")
        print("-" * 60)

    finally:
        env.close()


if __name__ == "__main__":
    run_smoke_test()