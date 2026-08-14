"""
Reward functions for the EcoFlux reinforcement learning agent.

The reward balances two objectives:
1. Reduce total CO2 emissions.
2. Reduce total vehicle waiting time.
"""


# Default weights are aligned with the baseline reward
# already used in Member-1's EcoTwinEnv.
DEFAULT_CO2_WEIGHT = 0.001
DEFAULT_WAITING_WEIGHT = 0.01


def calculate_reward(
    total_co2,
    total_waiting_time,
    co2_weight=DEFAULT_CO2_WEIGHT,
    waiting_weight=DEFAULT_WAITING_WEIGHT
):
    """
    Calculate the multi-objective RL reward.

    Lower CO2 and lower waiting time produce a higher reward.

    Parameters
    ----------
    total_co2 : float
        Total CO2 emission reported by SUMO.

    total_waiting_time : float
        Total vehicle waiting time reported by SUMO.

    co2_weight : float
        Weight assigned to CO2 penalty.

    waiting_weight : float
        Weight assigned to waiting-time penalty.

    Returns
    -------
    float
        Combined reward.
    """

    if total_co2 < 0:
        raise ValueError("total_co2 cannot be negative.")

    if total_waiting_time < 0:
        raise ValueError(
            "total_waiting_time cannot be negative."
        )

    if co2_weight < 0:
        raise ValueError(
            "co2_weight cannot be negative."
        )

    if waiting_weight < 0:
        raise ValueError(
            "waiting_weight cannot be negative."
        )

    co2_penalty = co2_weight * float(total_co2)
    waiting_penalty = waiting_weight * float(total_waiting_time)

    reward = -(co2_penalty + waiting_penalty)

    return float(reward)


def get_reward_components(
    total_co2,
    total_waiting_time,
    co2_weight=DEFAULT_CO2_WEIGHT,
    waiting_weight=DEFAULT_WAITING_WEIGHT
):
    """
    Return individual reward components for logging and evaluation.

    Returns
    -------
    dict
        CO2 penalty, waiting penalty and total reward.
    """

    co2_penalty = co2_weight * float(total_co2)
    waiting_penalty = waiting_weight * float(total_waiting_time)

    reward = -(co2_penalty + waiting_penalty)

    return {
        "co2_penalty": float(co2_penalty),
        "waiting_penalty": float(waiting_penalty),
        "reward": float(reward)
    }