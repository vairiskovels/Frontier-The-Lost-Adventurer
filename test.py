"""
TEST
"""

import sys, os
import pygame

pygame.init()


# ============ Variables ============
black = (0, 0, 0)
white = (255, 255, 255)
dark_blue = (12, 17, 34, 217)

clock = pygame.time.Clock()
FPS = 60


# ============ Main game class ============
class Game:
    def __init__(self):
        # Initialize game window
        self.screenWidth = 1280
        self.screenHeight = 720
        self.win = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.caption = pygame.display.set_caption("TEST")

        self.background = pygame.transform.scale(pygame.image.load("data/images/backgrounds/background.jpg"), (self.screenWidth, self.screenHeight))
        self.background_width, self.background_height = self.background.get_rect().size
        self.bg_x = 0


        # Defining game running
        self.running = True

        # Defining player
        self.player = Player(-100, 550)

        self.pause = False

        self.bg_vel = self.player.vel

    def run(self):

        while self.running:
            clock.tick(FPS)
            self.handle_keys()
            self.draw()
            self.player.move()

    def draw(self):
        self.draw_background()
        self.player.draw(self.win)

        pygame.display.update()

    def move_background(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.player.x <= 578:
            self.bg_x += self.bg_vel
            self.player.vel = 0

        elif keys[pygame.K_RIGHT] and self.player.x > 560:
            self.bg_x -= self.bg_vel
            self.player.vel = 0

    def draw_background(self):

        self.move_background()

        bg_rel_x = self.bg_x % self.background_width
        self.win.blit(self.background, (bg_rel_x - self.background_width, 0))
        if bg_rel_x < self.background_width:
            self.win.blit(self.background, (bg_rel_x, 0))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.pause:
                    self.pause = True
                elif event.key == pygame.K_ESCAPE and self.pause:
                    self.pause = False



player_idle_group = []

for i in range(0,15):
    if i < 10:
        player_idle_group.append(pygame.transform.scale(pygame.image.load(os.path.join("data/images/characters/Knight/idle", "tile00" + str(i) + ".png")), (144, 144)))
    else:
        player_idle_group.append(pygame.transform.scale(pygame.image.load(os.path.join("data/images/characters/Knight/idle", "tile0" + str(i) + ".png")), (144, 144)))

player_run_group = []

for i in range(0,8):
    player_run_group.append(pygame.transform.scale(pygame.image.load(os.path.join("data/images/characters/Knight/run", "tile00" + str(i) + ".png")), (144, 144)))

player_jump_group = []

for i in range(0,14):
    if i < 10:
        player_jump_group.append(pygame.transform.scale(pygame.image.load(os.path.join("data/images/characters/Knight/jump", "tile00" + str(i) + ".png")), (144, 144)))
    else:
        player_jump_group.append(pygame.transform.scale(pygame.image.load(os.path.join("data/images/characters/Knight/jump", "tile0" + str(i) + ".png")), (144, 144)))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.player_idle_images = player_idle_group[:]
        self.player_run_images = player_run_group[:]
        self.player_jump_images = player_jump_group[:]

        self.player_idle_flipped = []
        self.player_run_flipped = []
        self.player_jump_flipped = []

        self.idle_count = 0
        self.run_count = 0
        self.jump_count = 0

        self.x = x
        self.y = y

        self.idle = True
        self.run = False
        self.jump = False

        self.vel = 6

        for image in self.player_idle_images:
            self.player_idle_flipped.append(pygame.transform.flip(image, True, False))
        for image in self.player_run_images:
            self.player_run_flipped.append(pygame.transform.flip(image, True, False))
        for image in self.player_jump_images:
            self.player_jump_flipped.append(pygame.transform.flip(image, True, False))
        self.flipped = False

    def draw(self, win):
        self.idle_count += 1
        if self.idle_count >= len(self.player_idle_images) * 5:
            self.idle_count = 0

        self.run_count += 1
        if self.run_count >= len(self.player_run_images) * 5:
            self.run_count = 0

        self.jump_count += 1
        if self.jump_count >= len(self.player_jump_images) * 5:
            self.jump_count = 0

        if self.flipped:
            player_idle = self.player_idle_flipped[self.idle_count // 5]
            player_run = self.player_run_flipped[self.run_count // 5]
            player_jump = self.player_jump_flipped[self.jump_count // 5]
        else:
            player_idle = self.player_idle_images[self.idle_count // 5]
            player_run = self.player_run_images[self.run_count // 5]
            player_jump = self.player_jump_images[self.jump_count // 5]

        if self.idle == True:
            win.blit(player_idle, (self.x, self.y))
        if self.run == True:
            win.blit(player_run, (self.x, self.y))
        if self.jump == True:
            win.blit(player_jump, (self.x, self.y))


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel

            self.idle = False
            self.run = True
            self.jump = False

            self.flipped = True

        elif keys[pygame.K_RIGHT]:
            self.x += self.vel

            self.idle = False
            self.run = True
            self.jump = False

            self.flipped = False

        else:
            self.idle = True
            self.run = False
            self.jump = False

        self.start_behind_screen()

    def start_behind_screen(self):
        if self.x < 50: # 1280/2 - 144/2
            self.x += self.vel
            self.run = True
            self.idle = False



if __name__ == "__main__":
    game = Game()
    game.run()