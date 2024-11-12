import random
from enum import Enum
import time

class SnakeAction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class GridTiles(Enum):
    _FLOOR=0
    SNAKE=1
    FRUIT=2

    def  __str__(self):
        return self.name[:1]
    
class Snake:
    def __init__(self, grid_rows=10, grid_cols=10):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols

        self.reset()

    def reset(self, seed=None):
        random.seed(seed)
        
        initial_row = random.randint(0, self.grid_rows - 1)
        initial_col = random.randint(0, self.grid_cols - 1)
        self.snake_body = [[initial_row, initial_col]]
        
        possible_directions = []
        if initial_row > 0:
            possible_directions.append(SnakeAction.UP)
        if initial_row < self.grid_rows - 1:
            possible_directions.append(SnakeAction.DOWN)
        if initial_col > 0:
            possible_directions.append(SnakeAction.LEFT)
        if initial_col < self.grid_cols - 1:
            possible_directions.append(SnakeAction.RIGHT)
        
        self.direction = random.choice(possible_directions)
        
        while True:
            fruit_row = random.randint(0, self.grid_rows - 1)
            fruit_col = random.randint(0, self.grid_cols - 1)
            if [fruit_row, fruit_col] not in self.snake_body:
                self.fruit_pos = [fruit_row, fruit_col]
                break


    def perform_action(self, snake_action:SnakeAction) -> bool:
        if self.is_valid_action(snake_action):
            self.direction = snake_action

        new_head = self.snake_body[0][:]
        if self.direction == SnakeAction.LEFT:
            new_head[1] -= 1
        elif self.direction == SnakeAction.RIGHT:
            new_head[1] += 1
        elif self.direction == SnakeAction.UP:
            new_head[0] -= 1
        elif self.direction == SnakeAction.DOWN:
            new_head[0] += 1

        if (new_head[0] < 0 or new_head[0] >= self.grid_rows or
            new_head[1] < 0 or new_head[1] >= self.grid_cols or
            new_head in self.snake_body):
                return False
        self.snake_body.insert(0, new_head)

        if new_head == self.fruit_pos:
            self.fruit_pos = [
                random.randint(0, self.grid_rows - 1),
                random.randint(0, self.grid_cols - 1)
            ]
        else:
            self.snake_body.pop()

    def is_valid_action(self, snake_action: SnakeAction) -> bool:
        if self.direction == SnakeAction.LEFT:
            return snake_action in [SnakeAction.LEFT, SnakeAction.UP, SnakeAction.DOWN]
        elif self.direction == SnakeAction.RIGHT:
            return snake_action in [SnakeAction.RIGHT, SnakeAction.UP, SnakeAction.DOWN]
        elif self.direction == SnakeAction.UP:
            return snake_action in [SnakeAction.UP, SnakeAction.LEFT, SnakeAction.RIGHT]
        elif self.direction == SnakeAction.DOWN:
            return snake_action in [SnakeAction.DOWN, SnakeAction.LEFT, SnakeAction.RIGHT]
        return False


    def get_grid(self):
        grid = [[GridTiles._FLOOR for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]
        for segment in self.snake_body:
            grid[segment[0]][segment[1]] = GridTiles.SNAKE
        grid[self.fruit_pos[0]][self.fruit_pos[1]] = GridTiles.FRUIT
        return grid

    def render(self):

        grid = self.get_grid()
        for row in grid:
            print(" ".join(str(cell) for cell in row))
        print()
        time.sleep(0.5)
        print("\033[H\033[J", end="")


if __name__=="__main__":
    snake = Snake(grid_rows=7, grid_cols=7)
    snake.render()

    for i in range(100):
        valid_actions = [action for action in list(SnakeAction) if snake.is_valid_action(action)]
        rand_action = random.choice(valid_actions)

        print(rand_action)

        snake.perform_action(rand_action)
        snake.render()
