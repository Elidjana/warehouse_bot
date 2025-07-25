import numpy as np
import pygame
from config import *


class Warehouse:
    def __init__(self):
        # Grid values: 0-empty, 1-obstacle, 2-item
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

        # Simulate real shelves
        self.obstacles = []

        # Horizontal

        for row in [2, 5, 10]:
            for col in range(4, 11):
                self.obstacles.append((row, col))

        # Vertical

        for col in [10]:
            for row in range(2, 6):
                self.obstacles.append((row, col))
        for col in [4]:
            for row in range(5, 11):
                self.obstacles.append((row, col))

        # Obstacles in grid

        for y, x in self.obstacles:
            self.grid[y][x] = 1

        self.items = {  # items in shelf areas
            'green': [(5, 9)],
            'blue': [(5, 5)],
            'yellow': [(10, 6)]
        }

        for color, positions in self.items.items():
            for y, x in positions:
                self.grid[y][x] = 2  # Mark cell as item

    def draw(self, screen):

        item_colors = {
            'green': (0, 255, 0),
            'blue': (0, 100, 255),
            'yellow': (255, 255, 0)
        }

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y *
                                   CELL_SIZE, CELL_SIZE, CELL_SIZE)

                if self.grid[y][x] == 1:
                    color = OBSTACLES_COLOR
                elif self.grid[y][x] == 2:
                    # Determine the item color based on position
                    color = None
                    for c, positions in self.items.items():
                        if (y, x) in positions:
                            color = item_colors[c]
                            break
                    if not color:
                        color = ITEM_COLOR
                else:
                    color = EMPTY_COLOR

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (200, 200, 200),
                                 rect, 1)  # Grid lines

    def is_obstacle(self, pos):
        y, x = pos
        return self.grid[y][x] == 1

    def has_item(self, pos):
        y, x = pos
        return self.grid[y][x] == 2

    def get_items_by_color(self, color):
        return self.items.get(color, [])

    def remove_item_by_position(self, pos):
        """Removes the item from the grid and returns its color."""
        for color in self.items:
            if pos in self.items[color]:
                self.items[color].remove(pos)
                self.grid[pos[0]][pos[1]] = 0
                return color
        return None
