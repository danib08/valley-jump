"""
Valley Jump

Python 3.7.2
PyGame 1.9.4

Screens File
"""

from UI import *
import time

# Flags Dictionary
flags = {
	"Intro" : True,
	"Menu" : False,
	"Settings" : False,
	"Leaderboard" : False,
	"Game" : False,
    "Game Over" : False,
    "Win" : False,
	"Exit" : False
}

# Transparent Color
transColor = (255, 255, 255)

# ----- Intro -----
class IntroScreen:
    def __init__(self, frame, FPS, flags):
        self.frame = frame
        self.flags = flags
        self.time = 5 * FPS  # Time the Intro will appear

        # Animation
        self.spriteSheet = pygame.image.load("images/player_sprite.png")

        # Walking
        self.spriteSheet.set_clip(14, 161, 93, 99)
        walking1 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        walking1.set_colorkey(transColor)

        self.spriteSheet.set_clip(127, 161, 114, 102)
        walking2 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        walking2.set_colorkey(transColor)

        self.spriteSheet.set_clip(251, 163, 134, 100)
        walking3 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        walking3.set_colorkey(transColor)

        self.spriteSheet.set_clip(397, 164, 111, 104)
        walking4 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        walking4.set_colorkey(transColor)

        self.walking = [walking1, walking2, walking3, walking4]

        # Settings
        self.sprite = walking1
        self.sprite_index = -1
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (0, 300)
        self.animTime = time.time()

    # Exits the Intro and goes to the Menu
    def finish_intro(self):
        self.flags["Intro"] = False
        self.flags["Menu"] = True

    # Draws the animation on screen
    def draw(self):
        bg = pygame.image.load("images/intro_bg.png").convert_alpha()
        self.frame.blit(bg, (0, 0))
        self.frame.blit(self.sprite, (self.rect.left, self.rect.top))

    # Manages the movement and the time left
    def update(self):
        self.rect.left += 7
        self.sprite = self.get_sprite(self.walking).copy()

        if self.time <= 0:
            self.finish_intro()
        else:
            self.time -= 1

    # Returns one element to be displayed from a list of sprites
    def get_sprite(self, sprites):
        if time.time() - self.animTime >= 0.15:
            self.sprite_index += 1
            self.animTime = time.time()
            if self.sprite_index >= (len(sprites)):
                self.sprite_index = 0
        return sprites[self.sprite_index]

# ----- Menu -----
class MenuScreen:
    def __init__(self, frame, flags):
        self.frame = frame
        self.flags = flags

        # Creates all buttons
        self.buttons = [
        ScreenButton(self.frame, 350, 270, (72, 109, 66, 65), self.flags, "Menu", "Game"),
        ScreenButton(self.frame, 600, 270, (220, 922, 66, 67), self.flags, "Menu", "Leaderboard"),
        ScreenButton(self.frame, 860, 10, (146, 774, 66, 68), self.flags, "Menu", "Settings"),
        ScreenButton(self.frame, 930, 10, (664, 553, 66, 66), self.flags, "Menu", "Exit")
        ]

    # Draws backgroung image and buttons
    def draw(self):
        bg = pygame.image.load("images/menu_bg.png").convert()
        self.frame.blit(bg, (0, 0))
        
        for button in self.buttons:
            button.draw()


# ----- Settings Screen -----
class SettingsScreen:
    def __init__(self, frame, flags, gameScreen):
        self.frame = frame
        self.flags = flags
        self.gameScreen = gameScreen

        # Creates all buttons
        self.buttons = [
            LevelButton(self.frame, 400, 240, (146, 34, 66, 67), "easy", self.gameScreen),
            LevelButton(self.frame, 470, 240, (218, 34, 68, 67), "medium", self.gameScreen),
            LevelButton(self.frame, 540, 240, (71, 33, 68, 68), "hard", self.gameScreen),
            LivesButton(self.frame, 410, 340, (196, 40, 27, 38), 1, self.gameScreen),
            LivesButton(self.frame, 490, 340, (239, 80, 29, 38), 3, self.gameScreen),
            LivesButton(self.frame, 560, 340, (237, 162, 29, 38), 5, self.gameScreen),
            ScreenButton(self.frame, 3, 10, (367, 257, 67, 67), flags, "Settings", "Menu"),
            ]

    # Draws backgroung image and buttons
    def draw(self):
        bg = pygame.image.load("images/settings_bg.png").convert()
        self.frame.blit(bg, (0, 0))

        for button in self.buttons:
            button.draw()


# ----- Leaderboard Screen -----
class LeaderboardScreen:
    def __init__(self, frame, flags, scores_ints):
        self.frame = frame
        self.flags = flags
        self.scores_ints = scores_ints

        # Creates a button
        self.button = ScreenButton(self.frame, 460, 400, (367, 257, 67, 67), self.flags, "Leaderboard", "Menu")

    # Draws backgroung image, button and displays text
    def draw(self):
        bg = pygame.image.load("images/leaderboard_bg.png").convert()
        self.frame.blit(bg, (0, 0))
        self.button.draw()

        display_text(self.frame, str(self.scores_ints[0]), 40, 550, 200)
        display_text(self.frame, str(self.scores_ints[1]), 40, 550, 250)
        display_text(self.frame, str(self.scores_ints[2]), 40, 550, 300)


# ----- Game Over Screen -----
class GameOverScreen:
    def __init__(self, frame, flags):
        self.frame = frame
        self.flags = flags

        # Creates all buttons
        self.buttons = [
            ScreenButton(self.frame, 350, 330, (367, 257, 67, 67), self.flags, "Game Over", "Menu"),
            ScreenButton(self.frame, 600, 330, (220, 922, 66, 67), self.flags, "Game Over", "Leaderboard"),
            ScreenButton(self.frame, 930, 10, (664, 553, 66, 66), self.flags, "Game Over", "Exit")
        ]

    # Draws backgroung image and buttons
    def draw(self):
        bg = pygame.image.load("images/gameover_bg.png").convert()
        self.frame.blit(bg, (0, 0))

        for button in self.buttons:
            button.draw()


# ----- You Won Screen -----
class WinScreen:
    def __init__(self, frame, flags):
        self.frame = frame
        self.flags = flags

        # Creates all buttons
        self.buttons = [
            ScreenButton(self.frame, 350, 330, (367, 257, 67, 67), self.flags, "Win", "Menu"),
            ScreenButton(self.frame, 600, 330, (220, 922, 66, 67), self.flags, "Win", "Leaderboard"),
            ScreenButton(self.frame, 930, 10, (664, 553, 66, 66), self.flags, "Win", "Exit")
        ]

    # Draws backgroung image and buttons
    def draw(self):
        bg = pygame.image.load("images/win_bg.png").convert()
        self.frame.blit(bg, (0, 0))

        for button in self.buttons:
            button.draw()

# Quit
pygame.quit()
