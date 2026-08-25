"""
Reward functions for the EcoFlux reinforcement learning agent.

The reward balances:
1. CO2 reduction.
2. Waiting-time reduction.

The reward is based on CHANGE between consecutive
simulation states rather than raw cumulative totals.

This prevents large cumulative CO2 values from
dominating the waiting-time objective.
"""

from __future__ import annotations


# ============================================================
# NORMALIZATION CONSTANTS
# ============================================================

# Approximate scale used to normalize one-step changes.
#
# These are deliberately not extremely small because SUMO
# cumulative values can become large during an episode.

DEFAULT_CO2_SCALE = 1000.0

DEFAULT_WAITING_SCALE = 100.0


# ============================================================
# OBJECTIVE WEIGHTS
# ============================================================

# CO2 and waiting time are now balanced.

DEFAULT_CO2_WEIGHT = 0.45

DEFAULT_WAITING_WEIGHT = 0.55


# ============================================================
# REWARD CALCULATION
# ============================================================

def calculate_reward(
    total_co2,
    total_waiting_time,
    previous_co2=0.0,
    previous_waiting_time=0.0,
    co2_weight=DEFAULT_CO2_WEIGHT,
    waiting_weight=DEFAULT_WAITING_WEIGHT,
    co2_scale=DEFAULT_CO2_SCALE,
    waiting_scale=DEFAULT_WAITING_SCALE,
):
    """
    Calculate reward from changes in traffic metrics.

    A decrease in CO2 produces a positive reward.

    A decrease in waiting time produces a positive reward.

    An increase in either metric produces a negative reward.

    Parameters
    ----------
    total_co2 : float
        Current cumulative CO2 reported by SUMO.

    total_waiting_time : float
        Current cumulative waiting time reported by SUMO.

    previous_co2 : float
        CO2 value from the previous environment step.

    previous_waiting_time : float
        Waiting-time value from the previous environment step.

    co2_weight : float
        Weight assigned to CO2 improvement.

    waiting_weight : float
        Weight assigned to waiting-time improvement.

    co2_scale : float
        Normalization scale for CO2 change.

    waiting_scale : float
        Normalization scale for waiting-time change.

    Returns
    -------
    float
        Balanced step reward.
    """

    # ========================================================
    # VALIDATION
    # ========================================================

    total_co2 = float(total_co2)

    total_waiting_time = float(
        total_waiting_time
    )

    previous_co2 = float(
        previous_co2
    )

    previous_waiting_time = float(
        previous_waiting_time
    )

    co2_weight = float(
        co2_weight
    )

    waiting_weight = float(
        waiting_weight
    )

    co2_scale = float(
        co2_scale
    )

    waiting_scale = float(
        waiting_scale
    )

    if total_co2 < 0:
        raise ValueError(
            "total_co2 cannot be negative."
        )

    if total_waiting_time < 0:
        raise ValueError(
            "total_waiting_time cannot be negative."
        )

    if previous_co2 < 0:
        raise ValueError(
            "previous_co2 cannot be negative."
        )

    if previous_waiting_time < 0:
        raise ValueError(
            "previous_waiting_time cannot be negative."
        )

    if co2_weight < 0:
        raise ValueError(
            "co2_weight cannot be negative."
        )

    if waiting_weight < 0:
        raise ValueError(
            "waiting_weight cannot be negative."
        )

    if co2_scale <= 0:
        raise ValueError(
            "co2_scale must be greater than zero."
        )

    if waiting_scale <= 0:
        raise ValueError(
            "waiting_scale must be greater than zero."
        )

    # ========================================================
    # CALCULATE CHANGE
    # ========================================================

    # Positive value means the metric increased.
    co2_change = (
        total_co2 - previous_co2
    )

    waiting_change = (
        total_waiting_time
        - previous_waiting_time
    )

    # ========================================================
    # CONVERT CHANGE TO IMPROVEMENT
    # ========================================================

    # If CO2 decreases, improvement becomes positive.
    #
    # Example:
    #
    # previous = 5000
    # current  = 4000
    #
    # improvement = +1000

    co2_improvement = (
        previous_co2 - total_co2
    )

    waiting_improvement = (
        previous_waiting_time
        - total_waiting_time
    )

    # ========================================================
    # NORMALIZATION
    # ========================================================

    normalized_co2 = (
        co2_improvement / co2_scale
    )

    normalized_waiting = (
        waiting_improvement
        / waiting_scale
    )

    # ========================================================
    # WEIGHTED REWARD
    # ========================================================

    co2_reward = (
        co2_weight
        * normalized_co2
    )

    waiting_reward = (
        waiting_weight
        * normalized_waiting
    )

    reward = (
        co2_reward
        + waiting_reward
    )

    # ========================================================
    # SMALL STABILITY PENALTY
    # ========================================================

    # Penalize simultaneous worsening of both objectives.

    if (
        co2_change > 0
        and waiting_change > 0
    ):

        reward -= 0.05

    return float(reward)


# ============================================================
# REWARD COMPONENTS
# ============================================================

def get_reward_components(
    total_co2,
    total_waiting_time,
    previous_co2=0.0,
    previous_waiting_time=0.0,
    co2_weight=DEFAULT_CO2_WEIGHT,
    waiting_weight=DEFAULT_WAITING_WEIGHT,
    co2_scale=DEFAULT_CO2_SCALE,
    waiting_scale=DEFAULT_WAITING_SCALE,
):
    """
    Return detailed reward components.

    Useful for debugging and evaluation.
    """

    total_co2 = float(total_co2)

    total_waiting_time = float(
        total_waiting_time
    )

    previous_co2 = float(
        previous_co2
    )

    previous_waiting_time = float(
        previous_waiting_time
    )

    co2_change = (
        total_co2 - previous_co2
    )

    waiting_change = (
        total_waiting_time
        - previous_waiting_time
    )

    co2_improvement = (
        previous_co2 - total_co2
    )

    waiting_improvement = (
        previous_waiting_time
        - total_waiting_time
    )

    normalized_co2 = (
        co2_improvement
        / float(co2_scale)
    )

    normalized_waiting = (
        waiting_improvement
        / float(waiting_scale)
    )

    co2_reward = (
        float(co2_weight)
        * normalized_co2
    )

    waiting_reward = (
        float(waiting_weight)
        * normalized_waiting
    )

    stability_penalty = 0.0

    if (
        co2_change > 0
        and waiting_change > 0
    ):

        stability_penalty = 0.05

    reward = (
        co2_reward
        + waiting_reward
        - stability_penalty
    )

    return {
        "co2_change": float(
            co2_change
        ),

        "waiting_time_change": float(
            waiting_change
        ),

        "co2_improvement": float(
            co2_improvement
        ),

        "waiting_time_improvement": float(
            waiting_improvement
        ),

        "co2_reward": float(
            co2_reward
        ),

        "waiting_reward": float(
            waiting_reward
        ),

        "stability_penalty": float(
            stability_penalty
        ),

        "reward": float(
            reward
        ),
    }


__all__ = [
    "calculate_reward",
    "get_reward_components",
]