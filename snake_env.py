# snake_env.py

from snake import Snake, Food, UP, RIGHT, DOWN, LEFT


class SnakeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.done = False
        self.steps_since_food = 0
        self.total_steps = 0
        return self.get_state()

    def step(self, action):
        if self.done:
            return self.get_state(), 0, True


        self.steps_since_food += 1
        if self.steps_since_food >= 100:
            self.done = True
            return self.get_state(), -10, True


        self._apply_action(action)
        self.snake.move()

        reward = -0.5
        self.done = False

        if self.snake.hits_wall() or self.snake.collides_with_self():
            reward = -10
            self.done = True
            return self.get_state(), reward, self.done

        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 1
            self.food.respawn(self.snake.body)
            self.steps_since_food = 0
            reward = 10

        if self.steps_since_food > 15 * len(self.snake.body):
            reward = -10
            self.done = True

        return self.get_state(), reward, self.done

    def get_state(self):
        head_x, head_y = self.snake.head
        food_x, food_y = self.food.position

        danger_straight = self._danger_in_direction(self.snake.direction)
        danger_left = self._danger_in_direction(self._turn_left(self.snake.direction))
        danger_right = self._danger_in_direction(self._turn_right(self.snake.direction))

        dir_left = self.snake.direction == LEFT
        dir_right = self.snake.direction == RIGHT
        dir_up = self.snake.direction == UP
        dir_down = self.snake.direction == DOWN

        food_left = food_x < head_x
        food_right = food_x > head_x
        food_up = food_y < head_y
        food_down = food_y > head_y

        return [
            int(danger_straight),
            int(danger_left),
            int(danger_right),

            int(dir_left),
            int(dir_right),
            int(dir_up),
            int(dir_down),

            int(food_left),
            int(food_right),
            int(food_up),
            int(food_down),
        ]

    def _apply_action(self, action):
        """
        action:
          0 = straight
          1 = turn left
          2 = turn right
        """
        if action == 0:
            new_dir = self.snake.direction
        elif action == 1:
            new_dir = self._turn_left(self.snake.direction)
        elif action == 2:
            new_dir = self._turn_right(self.snake.direction)
        else:
            raise ValueError("Action must be 0, 1, or 2")

        self.snake.turn(new_dir)

    def _turn_left(self, direction):
        directions = [UP, LEFT, DOWN, RIGHT]
        idx = directions.index(direction)
        return directions[(idx + 1) % 4]

    def _turn_right(self, direction):
        directions = [UP, RIGHT, DOWN, LEFT]
        idx = directions.index(direction)
        return directions[(idx + 1) % 4]

    def _danger_in_direction(self, direction):
        head_x, head_y = self.snake.head
        dx, dy = direction
        next_pos = (head_x + dx, head_y + dy)

        x, y = next_pos

        hits_wall = x < 0 or x >= 30 or y < 0 or y >= 24
        hits_self = next_pos in self.snake.body[1:]

        return hits_wall or hits_self