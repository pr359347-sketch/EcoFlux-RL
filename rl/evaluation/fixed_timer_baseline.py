"""
EcoFlux RL - Fixed Timer Baseline

Runs SUMO using a simple fixed-time traffic-light policy.

Purpose:
    Compare traditional fixed-timer traffic control
    against the PPO RL agent.

Metrics:
    - Total CO2
    - Total waiting time
    - Vehicle count
    - Episode length

The same SUMO configuration and 100 simulation steps
are used as the baseline PPO experiment.
"""

from __future__ import annotations

import csv
import os

import traci

from simulation_state import get_rl_observation


# ============================================================
# Configuration
# ============================================================

SUMO_CONFIG = "citygrid.sumocfg"

MAX_STEPS = 100

# Change traffic-light phase after this many SUMO steps.
PHASE_DURATION = 10

RESULTS_DIR = os.path.abspath(
    os.path.join(
        "rl",
        "results"
    )
)

CSV_FILE = os.path.join(
    RESULTS_DIR,
    "fixed_timer_metrics.csv"
)


# ============================================================
# Start SUMO
# ============================================================

def start_sumo():
    """Start SUMO in headless mode."""

    if traci.isLoaded():
        traci.close()

    traci.start(
        [
            "sumo",
            "-c",
            SUMO_CONFIG
        ]
    )

    print("SUMO started.")

    tls_ids = list(
        traci.trafficlight.getIDList()
    )

    print(
        f"Traffic lights detected: {len(tls_ids)}"
    )

    return tls_ids


# ============================================================
# Apply fixed-time policy
# ============================================================

def apply_fixed_timer(
    tls_ids,
    current_phases
):
    """
    Apply the current fixed phase to every
    traffic light.

    Each traffic light keeps its current phase
    until PHASE_DURATION is reached.
    """

    for index, tls_id in enumerate(
        tls_ids
    ):

        phase = current_phases[index]

        traci.trafficlight.setPhase(
            tls_id,
            int(phase)
        )


# ============================================================
# Move to next phase
# ============================================================

def advance_phases(
    tls_ids,
    current_phases
):
    """
    Move every traffic light to its next
    available phase.
    """

    for index, tls_id in enumerate(
        tls_ids
    ):

        phase_count = len(
            traci.trafficlight.getAllProgramLogics(
                tls_id
            )[0].getPhases()
        )

        if phase_count <= 0:
            continue

        current_phases[index] = (
            current_phases[index] + 1
        ) % phase_count


# ============================================================
# Collect metrics
# ============================================================

def collect_metrics():
    """
    Collect the same core SUMO metrics used
    by the RL environment.
    """

    data = get_rl_observation()

    return {
        "total_co2": float(
            data["total_co2"]
        ),
        "total_waiting_time": float(
            data["total_waiting_time"]
        ),
        "vehicle_count": int(
            data["vehicle_count"]
        )
    }


# ============================================================
# Save CSV
# ============================================================

def save_results(
    metrics
):
    """Save fixed-timer results to CSV."""

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "policy",
                "steps",
                "total_co2",
                "total_waiting_time",
                "vehicle_count"
            ]
        )

        writer.writerow(
            [
                "fixed_timer",
                MAX_STEPS,
                metrics["total_co2"],
                metrics["total_waiting_time"],
                metrics["vehicle_count"]
            ]
        )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 65)
    print("EcoFlux RL - Fixed Timer Baseline")
    print("=" * 65)

    tls_ids = []

    try:

        # ----------------------------------------------------
        # Start SUMO
        # ----------------------------------------------------

        tls_ids = start_sumo()

        if not tls_ids:
            raise RuntimeError(
                "No traffic lights found in SUMO."
            )

        # ----------------------------------------------------
        # Initial simulation step
        # ----------------------------------------------------

        traci.simulationStep()

        # ----------------------------------------------------
        # Initial phases
        # ----------------------------------------------------

        current_phases = []

        for tls_id in tls_ids:

            current_phase = (
                traci.trafficlight.getPhase(
                    tls_id
                )
            )

            current_phases.append(
                int(current_phase)
            )

        print(
            f"Initial phases: {current_phases}"
        )

        # ----------------------------------------------------
        # Run fixed-timer simulation
        # ----------------------------------------------------

        for step in range(
            1,
            MAX_STEPS + 1
        ):

            # Apply current fixed phases
            apply_fixed_timer(
                tls_ids,
                current_phases
            )

            # Advance SUMO
            traci.simulationStep()

            # Change phases after fixed duration
            if (
                step % PHASE_DURATION == 0
                and step < MAX_STEPS
            ):

                advance_phases(
                    tls_ids,
                    current_phases
                )

            # Print progress every 10 steps
            if step % 10 == 0:

                metrics = collect_metrics()

                print(
                    f"Step {step:03d} | "
                    f"CO2: {metrics['total_co2']:.2f} | "
                    f"Waiting: "
                    f"{metrics['total_waiting_time']:.2f} | "
                    f"Vehicles: "
                    f"{metrics['vehicle_count']}"
                )

        # ----------------------------------------------------
        # Final metrics
        # ----------------------------------------------------

        final_metrics = collect_metrics()

        # Save CSV
        save_results(
            final_metrics
        )

        print("\n" + "=" * 65)
        print("FIXED TIMER BASELINE COMPLETED")
        print("=" * 65)

        print(
            f"CO2               : "
            f"{final_metrics['total_co2']:.2f}"
        )

        print(
            f"Waiting Time      : "
            f"{final_metrics['total_waiting_time']:.2f}"
        )

        print(
            f"Vehicle Count     : "
            f"{final_metrics['vehicle_count']}"
        )

        print(
            f"Steps             : "
            f"{MAX_STEPS}"
        )

        print(
            f"\nMetrics CSV:\n{CSV_FILE}"
        )

        print("=" * 65)

    except Exception as error:

        print("\n" + "=" * 65)
        print("FIXED TIMER BASELINE FAILED")
        print("=" * 65)

        print(
            f"{type(error).__name__}: {error}"
        )

        print("=" * 65)

        raise

    finally:

        if traci.isLoaded():
            traci.close()

        print("\nSUMO closed.")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()