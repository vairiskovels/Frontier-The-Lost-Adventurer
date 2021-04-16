"""
Game 'Frontier' made by Vairis Kovels @ 2020. All rights reserved
"""
import pygame


class Subtitle:
    def __init__(self, x, y, player_x):
        self.x = x
        self.y = y
        self.player_x = player_x
        self.line = []
        self.subtitle = []
        self.subtitle_coords = []

    def load(self):
        subtitles = open("resources/subtitles.txt", "r")
        lines = subtitles.readlines()

        for i in range(len(lines)):
            self.line.append(lines[i].rstrip('\n').split(','))

        for i in range(len(self.line)):
            self.subtitle.append(self.line[i][0])
            self.subtitle_coords.append(self.line[i][1].lstrip())

        for i in range(len(self.line)):
            print(self.subtitle[i])
            print(self.subtitle_coords[i])

    def draw(self):
        self.load()

        if self.player_x >= any(self.subtitle_coords):
            print(self.subtitle[0])



