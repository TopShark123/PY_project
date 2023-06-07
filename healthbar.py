import pygame

class HealthBar():
    def __init__(self, x, y, width, height, max_hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = max_hp
        self.max_hp = max_hp



    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def update(self, new_hp):
        self.hp = new_hp
        if self.hp < 0:
            self.hp = 0
        elif self.hp > self.max_hp:
            self.hp = self.max_hp

    def draw(self, win):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(win, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, "green", (self.x, self.y, self.width * ratio, self.height))

        