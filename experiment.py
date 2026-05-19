# random_experiment.py

import random
from snake_env import SnakeEnv


env = SnakeEnv()

episodes = 100

for episode in range(episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = random.randint(0, 2)
        next_state, reward, done = env.step(action)

        total_reward += reward
        state = next_state

    print(
        f"Episode {episode + 1} | "
        f"Score: {env.score} | "
        f"Reward: {total_reward:.2f}"
    )