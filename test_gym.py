from ecotwin_env import EcoTwinEnv


env = EcoTwinEnv()

observation, info = env.reset()

print("Initial observation:")
print(observation)

print("\nTraffic light phases:")
print(info["traffic_light_phases"])

action = env.action_space.sample()

print("\nRandom action:")
print(action)

observation, reward, terminated, truncated, info = env.step(action)

print("\nAfter one step:")
print("Observation:", observation)
print("Reward:", reward)
print("Terminated:", terminated)
print("Truncated:", truncated)

print("\nTraffic light phases after step:")
print(info["traffic_light_phases"])

env.close()

print("\nGym environment test completed!")
