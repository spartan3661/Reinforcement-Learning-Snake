import pygame
WINDOW_SIZE = 30

class SnakeRenderer:
    def __init__(self, env, cell_size=WINDOW_SIZE):
        pygame.init()
        self.env = env
        self.grid_rows = env.grid_rows
        self.grid_cols = env.grid_cols
        self.cell_size = cell_size
        self.window_size = (self.grid_cols * cell_size, self.grid_rows * cell_size)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Snake Game GUI")

        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.clock = pygame.time.Clock()

    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        grid = self.env.snake.get_grid()

        self.screen.fill(self.BLACK)

        # Draw the snake and the fruit correctly
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if grid[row][col].value == 1:  # SNAKE
                    pygame.draw.rect(self.screen, self.GREEN,
                                     pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
                elif grid[row][col].value == 2:  # FRUIT
                    pygame.draw.rect(self.screen, self.RED,
                                     pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

        pygame.display.flip()
        self.clock.tick(10)
