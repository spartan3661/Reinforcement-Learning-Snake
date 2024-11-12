import gymnasium as gym
import numpy as np
from snake_env import SnakeEnv
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
import time
CELL_SIZE = 10
# Hyperparameters
LEARNING_RATE = 0.0001
BUFFER_SIZE = 10000
BATCH_SIZE = 64
GAMMA = 0.99
TARGET_UPDATE_INTERVAL = 10
TRAINING_TIMESTEPS = 1000000
MODEL_SAVE_PATH = "snake_sb3_V1.zip"


env = DummyVecEnv([lambda: SnakeEnv(grid_rows=CELL_SIZE, grid_cols=CELL_SIZE)])

# Create the DQN model
model = DQN(
    "MlpPolicy",  # Policy network structure
    env,
    learning_rate=LEARNING_RATE,
    buffer_size=BUFFER_SIZE,
    batch_size=BATCH_SIZE,
    gamma=GAMMA,
    target_update_interval=TARGET_UPDATE_INTERVAL,
    verbose=0,  # Disable built-in verbose to use custom output
    device="auto"  # Automatically chooses 'cuda' if available
)

# Custom function to log training progress
def custom_training_info(timestep, episode_rewards, start_time):
    elapsed_time = time.time() - start_time
    avg_reward = np.mean(episode_rewards[-10:]) if len(episode_rewards) > 0 else 0
    print(f"\nTimestep: {timestep}")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")
    print(f"Average Reward (last 10 episodes): {avg_reward:.2f}")
    print(f"Episodes Completed: {len(episode_rewards)}")

# Train the model with custom verbose output
start_time = time.time()
episode_rewards = []
obs = env.reset()
total_timesteps = TRAINING_TIMESTEPS

for timestep in range(1, total_timesteps + 1):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, infos = env.step(action)
    
    # Record reward
    if len(episode_rewards) == 0 or dones[0]:  # `dones` is now an array
        episode_rewards.append(rewards[0])
    else:
        episode_rewards[-1] += rewards[0]

    # Reset environment when done
    if dones[0]:
        obs = env.reset()

    # Print custom training information at intervals
    if timestep % 1000 == 0:
        custom_training_info(timestep, episode_rewards, start_time)

# Save the trained model
model.save(MODEL_SAVE_PATH)
print(f"Model saved to {MODEL_SAVE_PATH}")

env.close()
