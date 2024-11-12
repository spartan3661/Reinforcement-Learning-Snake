import gymnasium as gym
from gymnasium import spaces
import numpy as np
from snake import Snake, SnakeAction
from gui import SnakeRenderer
import pygame
import time
import math

CELL_SIZE = 10

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human', 'gui']}

    def __init__(self, grid_rows=CELL_SIZE, grid_cols=CELL_SIZE, render_mode='human'):
        super(SnakeEnv, self).__init__()
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.snake = Snake(grid_rows=self.grid_rows, grid_cols=self.grid_cols)
        self.render_mode = render_mode

        if self.render_mode == 'gui':
            self.renderer = SnakeRenderer(self)
        else:
            self.renderer = None

        self.action_space = spaces.Discrete(4)

        self.observation_space = spaces.Box(low=0, high=2, shape=(self.grid_rows, self.grid_cols), dtype=np.int32)

        self.fruits_collected = 0
        self.previous_distance = None

    def reset(self, seed=None):
        self.snake.reset(seed=seed)
        self.fruits_collected = 0
        self.previous_distance = self._calculate_distance_to_fruit()
        return self._get_observation(), {}

    def step(self, action):
        snake_action = SnakeAction(action)
        valid_move = self.snake.is_valid_action(snake_action)

        if valid_move:
            self.snake.perform_action(snake_action)
        else:
            # Perform the current direction instead if the action is invalid
            self.snake.perform_action(self.snake.direction)

        head = self.snake.snake_body[0]
        done = (
            head[0] < 0 or head[0] >= self.grid_rows or
            head[1] < 0 or head[1] >= self.grid_cols or
            head in self.snake.snake_body[1:]
        )

        reward = self.calculate_reward(done, head, valid_move)
        observation = self._get_observation()
        return observation, reward, done, False, {}
    
    def calculate_reward(self, done, head, valid_move):
        if done:
            return -70
        elif head == self.snake.fruit_pos:
            self.fruits_collected += 1
            return 50
        else:
            current_distance = self._calculate_distance_to_fruit()
            if self.previous_distance is not None and current_distance < self.previous_distance:
                reward = 0.5
            else:
                reward = 0.05
            
            # Reduce reward if the chosen action was invalid
            if not valid_move:
                reward -= 0.1
            
            self.previous_distance = current_distance
            return reward

    def _calculate_distance_to_fruit(self):
        head = self.snake.snake_body[0]
        fruit = self.snake.fruit_pos
        # Using Manhattan distance as it fits better for grid environments
        distance = abs(head[0] - fruit[0]) + abs(head[1] - fruit[1])
        return distance

    def render(self, mode='human'):
        if mode == 'human':
            self.snake.render()
        elif mode == 'gui' and self.renderer:
            self.renderer.render()
        else:
            raise NotImplementedError(f"Render mode '{mode}' is not supported.")

    def _get_observation(self):
        grid = self.snake.get_grid()
        observation = np.array([[int(cell.value) for cell in row] for row in grid], dtype=np.int32)
        return observation

    def close(self):
        if self.renderer:
            pygame.quit()


if __name__ == "__main__":
    env = SnakeEnv(grid_rows=CELL_SIZE, grid_cols=CELL_SIZE, render_mode='gui')
    obs, _ = env.reset()

    done = False
    while not done:
        action = env.action_space.sample()
        obs, reward, done, _, _ = env.step(action)

        env.render(mode='gui')
        time.sleep(0.1)

    env.close()
