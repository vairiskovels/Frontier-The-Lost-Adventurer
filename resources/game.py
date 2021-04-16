"""
Game 'Frontier' made by Vairis Kovels @ 2020. All rights reserved
"""

import sys
import os
import pygame
import random
from resources.player import Player
from resources.subtitles import Subtitle

# Load enemies
from resources.skeleton import Skeleton

# ============ Initializing pygame ============
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# ============ Variables ============
black = (0, 0, 0)
white = (255, 255, 255)
dark_blue = (12, 17, 34, 128)
dark_green = (50, 168, 82)

clock = pygame.time.Clock()
FPS = 60

click_sound = pygame.mixer.Sound("data/sounds/click.wav")
click_sound.set_volume(0.1)

coin_image_1 = pygame.image.load(os.path.join("data/images", "coin.png"))
coin_image_2 = pygame.image.load(os.path.join("data/images", "coin2.png"))

weapon_res = (55, 55)
sword_image = pygame.transform.scale(
    pygame.image.load(os.path.join("data/images/characters/Knight/weapons", "sword.png")), weapon_res)
shield_image = pygame.transform.scale(
    pygame.image.load(os.path.join("data/images/characters/Knight/weapons", "shield.png")), weapon_res)


def play_music(music, vol):
    music = f"data/sounds/{music}.mp3"
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play()


def stop_music():
    pygame.mixer.music.stop()


def play_ambience():
    stop_music()
    music = "data/sounds/ambience.mp3"
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(2)
    pygame.mixer.music.play()


# ============ Main game class ============
class Game:
    def __init__(self):
        # Initialize game window
        self.screen_width = 1280
        self.screen_height = 720
        self.win = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.caption = pygame.display.set_caption("Frontier: The Lost Adventurer")

        # Defining player
        self.player = Player(-100, 535)

        # Defining game background
        self.bg1 = pygame.transform.scale(pygame.image.load("data/images/backgrounds/bg1.png"),
                                          (self.screen_width, self.screen_height))
        self.bg2 = pygame.transform.scale(pygame.image.load("data/images/backgrounds/bg2.png"),
                                          (self.screen_width, self.screen_height))
        self.bg3 = pygame.transform.scale(pygame.image.load("data/images/backgrounds/bg3.png"),
                                          (self.screen_width, self.screen_height))
        self.bg4 = pygame.transform.scale(pygame.image.load("data/images/backgrounds/bg4.png"),
                                          (self.screen_width, self.screen_height))
        self.bg5 = pygame.transform.scale(pygame.image.load("data/images/backgrounds/bg5.png"),
                                          (self.screen_width, self.screen_height))

        self.bg = pygame.transform.scale(pygame.image.load("data/images/backgrounds/background.jpg"),
                                         (self.screen_width, self.screen_height))

        self.background_width, self.background_height = self.bg.get_rect().size
        self.bg_x = 0
        self.bg_vel = self.player.vel

        # Defining font
        self.font = pygame.font.Font("data/fonts/mainFont.ttf", 42)
        self.sub_font = pygame.font.Font("data/fonts/mainFont.ttf", 30)
        self.small_font = pygame.font.Font("data/fonts/mainFont.ttf", 42)
        self.smaller_font = pygame.font.Font("data/fonts/mainFont.ttf", 28)
        self.big_font = pygame.font.Font("data/fonts/mainFont.ttf", 60)

        # Speed of font moving
        self.font_x = 0

        # Speed of credits moving
        self.credits_y = self.screen_height + 450

        # Load subtitles
        self.subtitle = Subtitle(500, 500, self.player.real_x)

        # Defining game running
        self.running = True

        # Foreground change
        self.foreground_change = False

        # Toggle pause
        self.pause = False

        # Toggle credits
        self.credits = False

        # Mouse button click
        self.click = False

        # clicking sound
        self.click_sound_effect = True

        # Credits text
        self.title_list = []
        self.name_list = []
        self.load_credits()

        self.draw_hud = True

        self.enemy = Skeleton(500, 500)

        self.enemy.x = self.enemy.x - self.player.rel_x

    def run(self):
        while self.running:
            clock.tick(FPS)
            self.handle_keys()
            self.draw()

    def draw(self):
        if not self.pause and not self.credits:
            self.backgrounds()
            self.player.draw(self.win)
            self.enemy.draw(self.win)
            self.background(self.bg1, 0.15)

            if self.player.hitbox_on:
                self.player.draw_hitbox(self.win)

            if self.draw_hud:
                self.display_hud()
            self.text()
        elif self.credits:
            self.draw_credits()
        else:
            self.menu()

        pygame.display.flip()

    def move_background(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.player.x <= 268 or keys[pygame.K_a] and self.player.x <= 268:  # 18
            self.bg_x += self.bg_vel
            self.player.vel = 0
            self.player.real_x -= round(6 / 10)

        elif keys[pygame.K_RIGHT] and self.player.x > 250 or keys[pygame.K_d] and self.player.x > 250:
            self.bg_x -= self.bg_vel
            self.player.vel = 0
            self.player.real_x += round(6 / 10)

    def background(self, background, speed):
        self.move_background()

        bg_rel_x = self.bg_x * speed % self.background_width
        self.win.blit(background, (bg_rel_x - self.background_width, 0))
        if bg_rel_x < self.background_width:
            self.win.blit(background, (bg_rel_x, 0))

    def backgrounds(self):
        self.background(self.bg5, 0.005)
        self.background(self.bg4, 0.007)
        self.background(self.bg3, 0.05)
        self.background(self.bg2, 0.13)

    def text(self):
        # Defining text
        header_label = self.font.render("FRONTIER:", True, white)
        sub_header_label = self.font.render("THE LOST ADVENTURER", True, white)
        continue_game_label = self.sub_font.render("PRESS ANY KEY TO CONTINUE...", True, white)

        # Drawing text
        if self.font_x < 400:
            self.win.blit(header_label, (self.screen_width / 2 - header_label.get_width() / 2, 95 - 1 * self.font_x))
            self.win.blit(sub_header_label,
                          (self.screen_width / 2 - sub_header_label.get_width() / 2, 145 - 1 * self.font_x))
            self.win.blit(continue_game_label,
                          (self.screen_width / 2 - sub_header_label.get_width() / 2, 672 + 1 * self.font_x))

        self.move_text()

    def move_text(self):
        # Moving speed of font on X-axis
        self.font_x += 17

    def menu(self):
        # If self.pause is True then this is toggled
        self.menu_box()
        self.menu_text()

    def menu_box(self):
        # Menu background
        s = pygame.Surface((self.screen_width, self.screen_height))  # the size of your rect  # alpha level
        s.fill(dark_blue)  # this fills the entire surface
        self.win.blit(s, (0, 0))  # (0,0) are the top-left coordinates

    def menu_text(self):
        # Defining menu text
        self.menu_label = self.big_font.render("MENU", True, white)
        self.options_label = self.small_font.render("OPTIONS", True, white)
        self.quit_label = self.small_font.render("QUIT", True, white)

        # Drawing menu text
        self.win.blit(self.menu_label, (75, 110))
        self.win.blit(self.options_label, (75, 500))
        self.win.blit(self.quit_label, (75, 555))

        self.menu_keys(self.options_label, 75, 500)
        self.menu_keys(self.quit_label, 75, 555)

    def menu_keys(self, name, x, y):
        # Getting mouse pos
        mx, my = pygame.mouse.get_pos()

        # Defining box
        menu_key_box = pygame.Rect(x - 4, y, name.get_width() + 4, name.get_height())
        pygame.draw.rect(self.win, dark_blue, menu_key_box, 1)

        # If mouse pos collides with box pox then box appears
        if menu_key_box.collidepoint((mx, my)):
            pygame.draw.rect(self.win, white, menu_key_box, 1)
            if self.click_sound_effect:
                self.click_sound_effect = False
                click_sound.play()

            # If it hits quit key, game quits
            if self.click and name == self.quit_label:
                pygame.quit()
                sys.exit()
        else:
            self.click_sound_effect = True

    def load_credits(self):
        game_credits = open("resources/credits.txt", "r")
        lines = game_credits.readlines()
        line = []

        for i in range(len(lines)):
            line.append(lines[i].rstrip('\n').split(','))

        for i in range(len(line)):
            self.title_list.append(line[i][0])
            self.name_list.append(line[i][1].lstrip())

    def draw_credits(self):
        # Credits background
        s = pygame.Surface((self.screen_width, self.screen_height))
        s.fill(dark_blue)
        self.win.blit(s, (0, 0))

        # Credit variables
        normal_size = 36
        small_size = 30

        title_x = self.screen_width / 2 + 50
        name_x = self.screen_width / 2 + 130

        self.credits_y -= 1

        # Draw title text
        self.draw_credit_text("FRONTIER", self.screen_width / 2 - 250, self.credits_y - 437, 110)
        self.draw_credit_text("THE LOST ADVENTURER", self.screen_width / 2 - 250, self.credits_y - 340, 45)

        # Draw credits text
        self.draw_credit_text("CREDITS", title_x, self.credits_y - 80, normal_size)

        for i in range(len(self.title_list)):
            self.draw_credit_text(self.title_list[i], title_x, self.credits_y + 80 * i, normal_size)
        for i in range(len(self.name_list)):
            self.draw_credit_text(self.name_list[i], name_x, self.credits_y + 5 + 80 * i, small_size)

    def draw_credit_text(self, text, x, y, font_size):
        font = pygame.font.Font("data/fonts/mainFont.ttf", font_size)
        label = font.render(text, True, white)
        if -100 < y <= self.screen_height:
            if x == self.screen_width / 2 + 50:
                self.win.blit(label, (x - label.get_width(), y))
            else:
                self.win.blit(label, (x, y))

        if text == self.title_list[-1] and y < -50:
            self.credits = False
            self.running = False
            play_ambience()

    def display_hud(self):
        self.coins()
        self.draw_box()

    def coins(self):
        # Money labels
        self.coins_label = self.smaller_font.render(str(self.player.money), True, white)
        self.gold_label = self.smaller_font.render(str(self.player.gold), True, white)

        # Money x-pos
        coin_image_x = 34
        coins_label_x = 70

        # Blit money to screen
        self.win.blit(self.coins_label,
                      (coins_label_x, 68 + coin_image_1.get_width() / 2 - self.coins_label.get_height() / 2))
        self.win.blit(self.gold_label,
                      (coins_label_x, 105 + coin_image_1.get_width() / 2 - self.gold_label.get_height() / 2))

        # Blit coin images to screen
        self.win.blit(coin_image_2, (coin_image_x, 65))
        self.win.blit(coin_image_1, (coin_image_x, 102))

        self.player.save_data()

    def draw_box(self):
        # Draws box; takes box x and y coordinates and box's width and height, box's color and outline color
        self.generate_box(34, 25, 227, 24)
        self.health()
        self.generate_outline(34, 25, 227, 24)

        self.generate_box(self.screen_width - 34 - 86, 25, 86, 86)
        self.generate_outline(self.screen_width - 34 - 86, 25, 86, 86)
        if not self.player.shield:
            self.draw_weapon(sword_image, (
                self.screen_width - 120 + 43 - sword_image.get_width() / 2, 25 + 43 - 3 - sword_image.get_height() / 2))
        elif self.player.shield:
            self.draw_weapon(shield_image, (self.screen_width - 120 + 43 + 2 - shield_image.get_width() / 2,
                                            25 + 43 - 3 - shield_image.get_height() / 2))

    def generate_box(self, bar_x, bar_y, bar_width, bar_height, color=(40, 40, 40, 97)):
        # Generates box
        bar = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        bar.fill(color)
        self.win.blit(bar, (bar_x, bar_y))

    def generate_outline(self, bar_x, bar_y, bar_width, bar_height, color=(50, 50, 50, 60)):
        # Generates outlines
        pygame.draw.rect(self.win, color, pygame.Rect(bar_x, bar_y, bar_width, bar_height), 2)

    def health(self):
        # Draws health bar
        bar_x = 34
        bar_y = 25
        bar_width = 227
        bar_height = 24
        color_bar_width = (self.player.hp * bar_width) / 100

        # Health bar colors
        r = 0
        g = 255
        b = 0

        if 100 > self.player.hp >= 50:
            r = int(5.1) * (100 - self.player.hp)
        elif 50 > self.player.hp > 0:
            r = 255
            g = 255 - int(5.1) * (50 - self.player.hp)

        # If player has health, the health bar shows up
        if self.player.hp > 0:
            pygame.draw.rect(self.win, (r, g, b), pygame.Rect(bar_x, bar_y, color_bar_width, bar_height))

    def draw_weapon(self, image, pos):
        self.win.blit(image, pos)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not self.player.attack and not self.credits:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                        if not self.pause:
                            self.player.attack = True
                        if not self.player.run:
                            self.player.play_sounds()
                    elif event.button == 3:
                        self.player.shield = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.click = False
                self.player.shield = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.pause and not self.credits:
                    self.pause = True
                elif event.key == pygame.K_ESCAPE and self.pause:
                    self.pause = False

                if event.key == pygame.K_c and not self.pause and not self.credits:
                    self.credits = True
                    stop_music()
                    play_music("8bit", 0.2)
                elif event.type == pygame.KEYDOWN and self.credits:
                    self.credits = False
                    self.credits_y = self.screen_height + 450
                    self.running = False
                    play_ambience()

                if event.key == pygame.K_r:
                    self.running = False

                if event.key == pygame.K_b and not self.player.hitbox_on:
                    self.player.hitbox_on = True
                elif event.key == pygame.K_b and self.player.hitbox_on:
                    self.player.hitbox_on = False

                if event.key == pygame.K_h and self.draw_hud:
                    self.draw_hud = False
                elif event.key == pygame.K_h and not self.draw_hud:
                    self.draw_hud = True

                if event.key == pygame.K_w and not self.foreground_change:
                    self.foreground_change = True
                    self.player.y = 530
                elif event.key == pygame.K_s and self.foreground_change:
                    self.foreground_change = False
                    self.player.y = 535

                if event.key == pygame.K_q and self.pause:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_t:
                    self.player.money += random.randint(3, 15)
                    self.player.gold += random.randint(3, 15)
                    self.player.hp += random.randint(3, 15)
                elif event.key == pygame.K_y:
                    self.player.money -= random.randint(3, 15)
                    self.player.gold -= random.randint(3, 15)
                    self.player.hp -= random.randint(3, 15)

        if not self.pause:
            self.player.move()
