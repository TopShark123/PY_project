import pygame

WIDTH, HEIGHT = 800,600
window = pygame.display.set_mode((WIDTH, HEIGHT))

class HealthBar():
    def __init__(self, x, y, width, height, max_hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = max_hp
        self.max_hp = max_hp

        
    def draw(self):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(window, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, "green", (self.x, self.y, self.width * ratio, self.height))

    def take_damage(self):
        self.hp -= 20
        if self.hp < 0:
            self.hp = 0

    def draw_update(self):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(window, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, "green", (self.x, self.y, self.width * ratio, self.height))