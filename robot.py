import pygame
from config import *


class Robot:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.carrying = False

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y *
                           CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, ROBOT_COLOR, rect)
