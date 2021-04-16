"""
Game 'Frontier' made by Vairis Kovels @ 2020. All rights reserved
"""

import pygame


class Enemy:
    def __init__(self):
        self.img = None
        self.imgs = []
        self.animationCount = 0
        self.flipped = False
        self.health = 1

    def collide(self, x, y):
        pass

    def draw(self, win):
        self.img = self.imgs[self.animationCount // 4]

        win.blit(self.img, (self.x - self.img.get_width() / 2, self.y - self.img.get_height() / 2 - 20))
        # self.draw_health_bar(win)

    def draw_health_bar(self, win):
        pass

    def move(self):
        pass

    def hit(self):
        pass
