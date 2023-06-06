import pygame
from object import Object
from os import listdir
from os.path import isfile, join

class Trap(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        path = join("assets","Traps", "Spikes", "Idle.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 0, width, height)
        surface.blit(image, (0, 0), rect)
        self.image.blit(image, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        pygame.transform.scale2x(surface)

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))