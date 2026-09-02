from app.simulation.sumo_client import sumo_client


def test_sumo_client():

    print("\nStarting SUMO through SumoClient...")

    sumo_client.start()

    try:
        print("SUMO connected successfully!")

        for step in range(10):
            sumo_client.simulation_step()

            simulation_time = sumo_client.get_time()
            vehicle_count = sumo_client.get_vehicle_count()

            print(
                f"Step {step + 1}: "
                f"time={simulation_time}, "
                f"vehicles={vehicle_count}"
            )

        print("SumoClient test completed successfully!")

    finally:
        sumo_client.close()


if __name__ == "__main__":
    test_sumo_client()