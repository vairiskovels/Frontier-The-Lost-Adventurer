"""
Game 'Frontier' made by Vairis Kovels @ 2020. All rights reserved
"""

import sys
import pygame
from resources.game import Game

# ============ Initializing pygame ============
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# ============ Variables ============
black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60

music = "data/sounds/ambience.mp3"
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(2)
pygame.mixer.music.play(-1)

pygame.mouse.set_cursor(*pygame.cursors.diamond)


# ============ Main menu class ============
class mainMenu:
    def __init__(self):
        # Initialize game window
        self.screenWidth = 1280
        self.screenHeight = 720
        self.win = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.caption = pygame.display.set_caption("Frontier: The Lost Adventurer")
        self.ico = pygame.display.set_icon(pygame.image.load("data/images/ico.png"))
        self.counter = 0

        # Defining game background
        self.background = pygame.transform.scale(pygame.image.load("data/images/backgrounds/background.jpg"),
                                                 (self.screenWidth, self.screenHeight)).convert_alpha()

        # Defining font
        self.font = pygame.font.Font("data/fonts/mainFont.ttf", 42)
        self.subFont = pygame.font.Font("data/fonts/mainFont.ttf", 30)

        # Defining game running
        self.running = True

    def run(self):

        while self.running:
            self.counter += 0.035

            self.handle_keys()
            self.draw()
            clock.tick(FPS)

    def draw(self):
        self.win.blit(self.background, (0, 0))
        self.text()
        pygame.display.flip()

    def text(self):
        # Defining text
        header = self.font.render("FRONTIER:", True, white)
        subHeader = self.font.render("THE LOST ADVENTURER", True, white)
        continueGame = self.subFont.render("PRESS ANY KEY TO CONTINUE...", True, white)

        # Drawing text
        self.win.blit(header, (self.screenWidth / 2 - header.get_width() / 2, 95))
        self.win.blit(subHeader, (self.screenWidth / 2 - subHeader.get_width() / 2, 145))
        # If counter % 2 is 0 then text blits
        if int(self.counter) % 2 == 0:
            self.win.blit(continueGame, (self.screenWidth / 2 - subHeader.get_width() / 2, 672))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game = Game()
                game.run()
