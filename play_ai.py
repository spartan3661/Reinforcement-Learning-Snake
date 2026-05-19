# play_ai.py

import torch
import pygame

from snake import Game, UP, DOWN, LEFT, RIGHT
from agent import Agent


DIRECTIONS = [RIGHT, DOWN, LEFT, UP]


class AIGame(Game):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    def get_state(self):
        head_x, head_y = self.snake.head
        food_x, food_y = self.food.position
        direction = self.snake.direction

        dir_l = direction == LEFT
        dir_r = direction == RIGHT
        dir_u = direction == UP
        dir_d = direction == DOWN

        point_l = (head_x - 1, head_y)
        point_r = (head_x + 1, head_y)
        point_u = (head_x, head_y - 1)
        point_d = (head_x, head_y + 1)

        state = [
            # danger straight
            (dir_r and self.is_collision(point_r)) or
            (dir_l and self.is_collision(point_l)) or
            (dir_u and self.is_collision(point_u)) or
            (dir_d and self.is_collision(point_d)),

            # danger right
            (dir_u and self.is_collision(point_r)) or
            (dir_d and self.is_collision(point_l)) or
            (dir_l and self.is_collision(point_u)) or
            (dir_r and self.is_collision(point_d)),

            # danger left
            (dir_d and self.is_collision(point_r)) or
            (dir_u and self.is_collision(point_l)) or
            (dir_r and self.is_collision(point_u)) or
            (dir_l and self.is_collision(point_d)),

            # current direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # food location
            food_x < head_x,
            food_x > head_x,
            food_y < head_y,
            food_y > head_y,
        ]

        return [int(x) for x in state]

    def is_collision(self, point):
        x, y = point

        if x < 0 or x >= 30 or y < 0 or y >= 24:
            return True

        if point in self.snake.body[1:]:
            return True

        return False

    def action_to_direction(self, action):
        """
        action 0 = straight
        action 1 = turn right
        action 2 = turn left
        """

        current_direction = self.snake.direction
        idx = DIRECTIONS.index(current_direction)

        if action == 0:
            new_dir = DIRECTIONS[idx]
        elif action == 1:
            new_dir = DIRECTIONS[(idx + 1) % 4]
        else:
            new_dir = DIRECTIONS[(idx - 1) % 4]

        return new_dir

    def _update(self):
        state = self.get_state()
        action = self.agent.choose_action(state)
        direction = self.action_to_direction(action)

        self.snake.turn(direction)

        super()._update()


if __name__ == "__main__":
    state_size = 11
    action_size = 3

    agent = Agent(state_size, action_size)

    agent.model.load_state_dict(torch.load("snake_dqn.pth"))
    agent.model.eval()

    agent.epsilon = 0.0

    game = AIGame(agent)
    game.run()