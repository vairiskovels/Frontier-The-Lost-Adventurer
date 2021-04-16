"""
Game 'Frontier' made by Vairis Kovels @ 2020. All rights reserved
"""

import pygame, os
import random

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


sprite_size = 168

player_idle_group = []
player_run_group = []
player_jump_group = []
player_attack_group = []
player_shield_group = []

# Upload idle sprites
for i in range(0, 19):
    if i < 10:
        player_idle_group.append(pygame.transform.scale(
            pygame.image.load(os.path.join("data/images/characters/Knight/idle", "tile00" + str(i) + ".png")),
            (sprite_size, sprite_size)))
    else:
        player_idle_group.append(pygame.transform.scale(
            pygame.image.load(os.path.join("data/images/characters/Knight/idle", "tile0" + str(i) + ".png")),
            (sprite_size, sprite_size)))

# Upload running sprites
for i in range(0, 8):
    player_run_group.append(pygame.transform.scale(
        pygame.image.load(os.path.join("data/images/characters/Knight/run", "tile00" + str(i) + ".png")),
        (sprite_size, sprite_size)))

# Upload jumping sprites
for i in range(0, 14):
    if i < 10:
        player_jump_group.append(pygame.transform.scale(
            pygame.image.load(os.path.join("data/images/characters/Knight/jump", "tile00" + str(i) + ".png")),
            (sprite_size, sprite_size)))
    else:
        player_jump_group.append(pygame.transform.scale(
            pygame.image.load(os.path.join("data/images/characters/Knight/jump", "tile0" + str(i) + ".png")),
            (sprite_size, sprite_size)))

# Upload attacking sprites
for i in range(15, 20):
    if i < 10:
        player_attack_group.append(pygame.transform.scale(
            pygame.image.load(os.path.join("data/images/characters/Knight/attack", "tile00" + str(i) + ".png")),
            (sprite_size, sprite_size)))
    else:
        player_attack_group.append(pygame.transform.scale(
            pygame.image.load(os.path.join("data/images/characters/Knight/attack", "tile0" + str(i) + ".png")),
            (sprite_size, sprite_size)))

# Upload shield sprites
for i in range(0, 7):
    player_shield_group.append(pygame.transform.scale(
        pygame.image.load(os.path.join("data/images/characters/Knight/shield", "tile00" + str(i) + ".png")),
        (sprite_size, sprite_size)))


# Sound effects
sword_swing1 = pygame.mixer.Sound("data/sounds/sword1.wav")
sword_swing2 = pygame.mixer.Sound("data/sounds/sword2.wav")
sword_swing3 = pygame.mixer.Sound("data/sounds/sword3.wav")
footstep_sound1 = pygame.mixer.Sound("data/sounds/footstep1.wav")
footstep_sound2 = pygame.mixer.Sound("data/sounds/footstep2.wav")

sword_swing1.set_volume(0.4)
sword_swing2.set_volume(0.2)
sword_swing3.set_volume(0.4)
footstep_sound1.set_volume(0.2)
footstep_sound2.set_volume(0.2)

with open('data/USERDATA.md', 'r') as fp:  # opens file with score in it
    line = fp.readlines()
    money_count = int(line[0])
    gold_count = int(line[1])
    hp = int(line[2])

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Position
        self.x = x
        self.y = y
        self.rel_x = 0
        self.rel_vel = 6

        if self.x < 260:
            self.real_x = round(self.x / 10)

        # Attaching sprites to variables
        self.player_idle_images = player_idle_group[:]
        self.player_run_images = player_run_group[:]
        self.player_jump_images = player_jump_group[:]
        self.player_attack_images = player_attack_group[:]
        self.player_shield_images = player_shield_group[:]

        # Hit box
        self.hitbox = (self.x, self.y, 144, 144)
        self.hitbox_on = False

        # Making sprites flipped
        self.player_idle_flipped = []
        self.player_run_flipped = []
        self.player_jump_flipped = []
        self.player_attack_flipped = []
        self.player_shield_flipped = []

        # Flipped status
        self.flipped = False

        # Can move after coming from behind the screen
        self.can_move = True

        # Sprite movement count
        self.idle_count = 0
        self.run_count = 0
        self.jump_count = 0
        self.attack_count = 0
        self.shield_count = 0

        # Movement status
        self.idle = True
        self.run = False
        self.jump = False
        self.attack = False
        self.shield = False

        # Player following mouse position
        self.player_mouse_follow = True

        # Velocity
        self.vel = 6

        # Animation speed
        self.animation_speed = 4

        # Player money
        self.money = money_count
        self.gold = gold_count

        # Player health
        self.hp = hp

        # Attaching each image to flipped
        for image in self.player_idle_images:
            self.player_idle_flipped.append(pygame.transform.flip(image, True, False))
        for image in self.player_run_images:
            self.player_run_flipped.append(pygame.transform.flip(image, True, False))
        for image in self.player_jump_images:
            self.player_jump_flipped.append(pygame.transform.flip(image, True, False))
        for image in self.player_attack_images:
            self.player_attack_flipped.append(pygame.transform.flip(image, True, False))
        for image in self.player_shield_images:
            self.player_shield_flipped.append(pygame.transform.flip(image, True, False))

    def draw(self, win):
        self.start_behind_screen()

        # Sprite movement count
        self.idle_count += 1
        if self.idle_count >= len(self.player_idle_images) * self.animation_speed:
            self.idle_count = 0

        self.run_count += 1
        if self.run_count >= len(self.player_run_images) * self.animation_speed:
            self.run_count = 0

        self.jump_count += 1
        if self.jump_count >= len(self.player_jump_images) * self.animation_speed:
            self.jump_count = 0

        self.attack_count += 1
        if self.attack_count >= len(self.player_attack_images) * self.animation_speed:
            self.attack_count = 0
            self.attack = False

        if self.shield_count < 20:
            self.shield_count += 1

        # If flipped then image is flipped
        if self.flipped:
            player_idle = self.player_idle_flipped[self.idle_count // self.animation_speed]
            player_run = self.player_run_flipped[self.run_count // self.animation_speed]
            player_jump = self.player_jump_flipped[self.jump_count // self.animation_speed]
            player_attack = self.player_attack_flipped[self.attack_count // self.animation_speed]
            player_shield = self.player_shield_flipped[self.shield_count // self.animation_speed]
        else:
            player_idle = self.player_idle_images[self.idle_count // self.animation_speed]
            player_run = self.player_run_images[self.run_count // self.animation_speed]
            player_jump = self.player_jump_images[self.jump_count // self.animation_speed]
            player_attack = self.player_attack_images[self.attack_count // self.animation_speed]
            player_shield = self.player_shield_images[self.shield_count // self.animation_speed]

        # Drawing sprites on the screen
        if self.idle:
            win.blit(player_idle, (self.x, self.y))
        if self.run:
            win.blit(player_run, (self.x, self.y))
            self.play_sounds()
        if self.jump:
            win.blit(player_jump, (self.x, self.y))
        if self.attack:
            win.blit(player_attack, (self.x, self.y))
        if self.shield:
            win.blit(player_shield, (self.x, self.y))

    def draw_hitbox(self, win):
        if not self.flipped:
            self.hitbox = (self.x + 48, self.y + 32, 84, 84)
            self.attack_hitbox = (self.x + 15, self.y + 5, 150, 125)
        else:
            self.hitbox = (self.x + 33, self.y + 32, 84, 84)
            self.attack_hitbox = (self.x, self.y + 5, 150, 125)

        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(win, (198, 72, 247), self.attack_hitbox, 2)

    def play_sounds(self):
        sword_swing_sounds = [sword_swing1, sword_swing2, sword_swing3]
        if self.attack:
            sword_swing_sounds[random.randint(0, len(sword_swing_sounds) - 1)].play()

        footstep_sounds = [footstep_sound1, footstep_sound2]
        if self.run:
            footstep_sounds[random.randint(0, len(footstep_sounds) - 1)].play()

    def save_data(self):
        with open('data/USERDATA.md', 'w+') as fp:
            fp.write(str(f"{self.money}"+"\n"))
            fp.write(str(f"{self.gold}"+"\n"))
            fp.write(str(f"{self.hp}"))

    def move(self):

        if self.attack and self.player_mouse_follow or self.shield and self.player_mouse_follow:
            self.mouse_movement()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.vel
            # For enemy moving
            self.rel_x += self.rel_vel

            self.idle = False
            self.run = True
            self.jump = False
            self.attack = False
            self.shield = False

            self.flipped = True

        elif keys[pygame.K_d] and not self.can_move or keys[pygame.K_RIGHT] and not self.can_move:
            self.x += self.vel
            # For enemy moving
            self.rel_x -= self.rel_vel

            self.idle = False
            self.run = True
            self.jump = False
            self.attack = False
            self.shield = False

            self.flipped = False

        elif self.attack:
            self.idle = False
            self.run = False
            self.jump = False
            self.shield = False

        elif self.shield:
            self.idle = False
            self.run = False
            self.jump = False
            self.attack = False

        else:
            self.idle = True
            self.run = False
            self.jump = False
            self.attack = False
            self.shield = False

            self.attack_count = 0

        if not self.jump:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.jump = True
                self.idle = False
                self.run = False
                self.attack = False
                self.shield = False
                self.idle_count = 0
        else:
            if self.jump_count >= 28:
                self.y -= (self.jump_count * abs(self.jump_count)) * 5
                self.jump_count -= 1
                self.idle = False
                self.run = False
                self.attack = False
                self.shield = False
            else: 
                self.jump_count = -28
                self.jump = False

    def mouse_movement(self):
        mx, my = pygame.mouse.get_pos()

        if mx < self.x + sprite_size / 2:
            self.flipped = True
        else:
            self.flipped = False

    def start_behind_screen(self):
        if self.x < 250 and self.can_move:
            self.x += self.vel
            self.run = True
            self.idle = False
            self.attack = False
        if self.x >= 250:
            self.can_move = False
