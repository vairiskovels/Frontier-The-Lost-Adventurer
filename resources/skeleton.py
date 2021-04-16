import pygame
import os
from resources.enemy import Enemy

imgs = []

for x in range(12):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("data/images/characters/Skeleton", "tile0" + add_str + ".png")),
        (60, 90)))


class Skeleton(Enemy):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.name = "skeleton"
        self.money = 4
        self.max_health = 4
        self.health = self.max_health
        self.imgs = imgs[:]
