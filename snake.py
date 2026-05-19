"""
Snake Game
----------
A classic Snake game built with Python and Pygame.

Controls:
  Arrow keys or WASD  — move
  P                   — pause / unpause
  R                   — restart (after game over)
  Q / Escape          — quit

Requirements:
  pip install pygame
"""

import sys
import random
import pygame

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CELL = 20          # size of each grid cell in pixels
COLS = 30          # grid columns
ROWS = 24          # grid rows
WIDTH  = COLS * CELL
HEIGHT = ROWS * CELL
FPS    = 12        # base frames per second (game speed)

# Colours
BLACK      = (  0,   0,   0)
DARK_GREY  = ( 20,  20,  20)
GREEN      = ( 60, 200,  80)
DARK_GREEN = ( 30, 130,  50)
RED        = (220,  50,  50)
WHITE      = (240, 240, 240)
GREY       = ( 80,  80,  80)
YELLOW     = (240, 200,  40)
BG_COLOR   = ( 12,  12,  12)
GRID_COLOR = ( 22,  22,  22)

# Directions (dx, dy)
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


# ---------------------------------------------------------------------------
# Game classes
# ---------------------------------------------------------------------------

class Snake:
    """Represents the player-controlled snake."""

    def __init__(self):
        # Start in the middle, moving right, length 3
        cx, cy = COLS // 2, ROWS // 2
        self.body: list[tuple[int, int]] = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.grew = False

    # --- Public interface ---

    def turn(self, new_dir: tuple[int, int]) -> None:
        """Queue a direction change; forbid 180° reversals."""
        if new_dir != OPPOSITE[self.direction]:
            self.pending_direction = new_dir

    def move(self) -> tuple[int, int]:
        """Advance by one cell; return the new head position."""
        self.direction = self.pending_direction
        head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1],
        )
        self.body.insert(0, head)
        if self.grew:
            self.grew = False
        else:
            self.body.pop()
        return head

    def hits_wall(self) -> bool:
        x, y = self.body[0]
        return not (0 <= x < COLS and 0 <= y < ROWS)

    def grow(self) -> None:
        self.grew = True

    def collides_with_self(self) -> bool:
        return self.body[0] in self.body[1:]

    @property
    def head(self) -> tuple[int, int]:
        return self.body[0]


class Food:
    """Manages food placement on the grid."""

    def __init__(self, snake_body: list[tuple[int, int]]):
        self.position = self._random_position(snake_body)

    def _random_position(self, occupied: list[tuple[int, int]]) -> tuple[int, int]:
        occupied_set = set(occupied)
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in occupied_set]
        return random.choice(free) if free else (0, 0)

    def respawn(self, snake_body: list[tuple[int, int]]) -> None:
        self.position = self._random_position(snake_body)


class Game:
    """Orchestrates the full game loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font_large  = pygame.font.SysFont("monospace", 48, bold=True)
        self.font_medium = pygame.font.SysFont("monospace", 28, bold=True)
        self.font_small  = pygame.font.SysFont("monospace", 18)
        self._new_game()

    def _new_game(self) -> None:
        self.snake  = Snake()
        self.food   = Food(self.snake.body)
        self.score  = 0
        self.paused = False
        self.over   = False


    # --- Main loop ---

    def run(self) -> None:
        while True:
            self._handle_events()
            if not self.paused and not self.over:
                self._update()
            self._draw()
            self.clock.tick(FPS)

    # --- Event handling ---

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self._quit()

                if self.over:
                    if event.key == pygame.K_r:
                        self._new_game()
                    continue

                if event.key == pygame.K_p:
                    self.paused = not self.paused

                # Movement keys (only meaningful when not paused)
                if not self.paused:
                    key_map = {
                        pygame.K_UP:    UP,
                        pygame.K_w:     UP,
                        pygame.K_DOWN:  DOWN,
                        pygame.K_s:     DOWN,
                        pygame.K_LEFT:  LEFT,
                        pygame.K_a:     LEFT,
                        pygame.K_RIGHT: RIGHT,
                        pygame.K_d:     RIGHT,
                    }
                    if event.key in key_map:
                        self.snake.turn(key_map[event.key])

    # --- Game logic ---

    def _update(self) -> None:
        self.snake.move()

        if self.snake.hits_wall() or self.snake.collides_with_self():
            self.over = True
            return

        if self.snake.head == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food.respawn(self.snake.body)

    # --- Drawing ---

    def _draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self._draw_grid()
        self._draw_food()
        self._draw_snake()
        self._draw_hud()

        if self.paused:
            self._draw_overlay("PAUSED", "Press P to continue")
        if self.over:
            self._draw_overlay("GAME OVER", f"Score: {self.score}   |   Press R to restart")

        pygame.display.flip()

    def _draw_grid(self) -> None:
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))

    def _draw_snake(self) -> None:
        for i, (x, y) in enumerate(self.snake.body):
            rect = pygame.Rect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2)
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            # Eyes on the head
            if i == 0:
                self._draw_eyes(x, y)

    def _draw_eyes(self, gx: int, gy: int) -> None:
        dx, dy = self.snake.direction
        cx = gx * CELL + CELL // 2
        cy = gy * CELL + CELL // 2

        # Offset eyes perpendicular to direction
        perp = (-dy, dx)  # 90° rotation
        for sign in (+1, -1):
            ex = cx + sign * perp[0] * 5 + dx * 4
            ey = cy + sign * perp[1] * 5 + dy * 4
            pygame.draw.circle(self.screen, WHITE, (ex, ey), 3)
            pygame.draw.circle(self.screen, BLACK, (ex + dx, ey + dy), 1)

    def _draw_food(self) -> None:
        fx, fy = self.food.position
        center = (fx * CELL + CELL // 2, fy * CELL + CELL // 2)
        pygame.draw.circle(self.screen, RED, center, CELL // 2 - 2)
        # Little shine dot
        pygame.draw.circle(self.screen, YELLOW, (center[0] - 3, center[1] - 3), 2)

    def _draw_hud(self) -> None:
        label = self.font_small.render(f"SCORE  {self.score:>6}", True, GREY)
        self.screen.blit(label, (8, 4))

    def _draw_overlay(self, title: str, subtitle: str) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        t = self.font_large.render(title, True, WHITE)
        s = self.font_medium.render(subtitle, True, GREY)
        self.screen.blit(t, t.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
        self.screen.blit(s, s.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 24)))

    @staticmethod
    def _quit() -> None:
        pygame.quit()
        sys.exit()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    Game().run()