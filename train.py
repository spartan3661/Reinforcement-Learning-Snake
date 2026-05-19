# train.py
import torch
from snake_env import SnakeEnv
from agent import Agent


env = SnakeEnv()

state_size = 11
action_size = 3

agent = Agent(state_size, action_size)

episodes = 1000
scores = []

for episode in range(episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.choose_action(state)

        next_state, reward, done = env.step(action)

        agent.remember(state, action, reward, next_state, done)
        agent.train_step()

        state = next_state
        total_reward += reward

    agent.decay_epsilon()
    scores.append(env.score)

    avg_score = sum(scores[-100:]) / min(len(scores), 100)

    print(
        f"Episode {episode + 1} | "
        f"Score: {env.score} | "
        f"Avg Score: {avg_score:.2f} | "
        f"Reward: {total_reward:.2f} | "
        f"Epsilon: {agent.epsilon:.3f}"
    )


torch.save(agent.model.state_dict(), "snake_dqn.pth")
print("Saved model to snake_dqn.pth")