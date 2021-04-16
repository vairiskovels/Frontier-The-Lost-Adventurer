"""import pygame, sys

pygame.init()


black = (0, 0, 0)
white = (255, 255, 255)
dark_blue = (12, 17, 34, 150)
random = (73,9,156,128)

clock = pygame.time.Clock()
FPS = 60

class mainMenu:
    def __init__(self):
        self.screenWidth = 1280
        self.screenHeight = 720
        self.win = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.caption = pygame.display.set_caption("Frontier: The Lost Adventurer")

        # Defining game background
        self.background = pygame.transform.scale(pygame.image.load("background.jpg"), (self.screenWidth, self.screenHeight))

        self.big_font = pygame.font.Font("mainFont.ttf", 55)
        self.small_font = pygame.font.Font("mainFont.ttf", 42)

    def run(self):
        running = True

        while running:
            clock.tick(FPS)
            self.handle_keys()
            self.draw()

    def draw(self):
        self.win.blit(self.background, (0, 0))
        self.box()
        self.text()
        pygame.display.update()

    def text(self):
        # Defining text
        menu_label = self.big_font.render("MENU", True, white)
        options_label = self.small_font.render("OPTIONS", True, white)
        quit_label = self.small_font.render("QUIT", True, white)

        # Drawing text
        self.win.blit(menu_label, (self.screenWidth / 2 - menu_label.get_width() / 2, 210))
        self.win.blit(options_label, (self.screenWidth / 2 - options_label.get_width() / 2, 397))
        self.win.blit(quit_label, (self.screenWidth / 2 - quit_label.get_width() / 2, 450))

    def box(self):

        pos = self.screenWidth / 2, self.screenHeight / 2

        s = pygame.Surface((0, 0), pygame.SRCALPHA, 32)  # per-pixel alpha
        s.fill(random)  # notice the alpha value in the color
        self.win.blit(s, pos)

        main_box = pygame.Rect(self.screenWidth / 2 - 350 / 2, self.screenHeight / 2 - 350 / 2, 350, 350)
        pygame.draw.rect(self.win, white, main_box, 2)

        '''main_box = pygame.Rect(self.screenWidth / 2 - 350 / 2, self.screenHeight / 2 - 350 / 2, 350, 350)
        pygame.draw.rect(self.win, dark_blue, main_box)'''

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    menu = mainMenu()
    menu.run()

"""