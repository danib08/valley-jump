"""
Valley Jump

Python 3.7.2
PyGame 1.9.4

User Interface File
"""

import pygame

# Function that displays text on the screen
def display_text(frame, message, size, x, y):
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(message, True, (0, 0, 0))
    frame.blit(text, (x, y))


# Button that changes screen
class ScreenButton:
    def __init__(self, frame, x, y, sprite_slice, flags, flagFalse, flagTrue):
        self.frame = frame
        self.image = "images/buttons.png"
        self.x = x
        self.y = y
        self.sprite_slice = sprite_slice
        self.flags = flags
        self.flagFalse = flagFalse
        self.flagTrue = flagTrue


    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        image_load = pygame.image.load(self.image).convert_alpha()
        self.frame.blit(image_load, (self.x, self.y), self.sprite_slice)

        # Checks if the image is being clicked
        if self.x < mouse[0] < self.x + self.sprite_slice[2] and self.y < mouse[1] < self.y + self.sprite_slice[3] and \
                click[0] == 1:
            self.flags[self.flagFalse] = False   # Exits the actual window
            self.flags[self.flagTrue] = True     # Makes the desired window appear


# Button that changes the level
class LevelButton:
    def __init__(self, frame, x, y, sprite_slice, difficulty, gameScreen):
        self.frame = frame
        self.image = "images/buttons.png"
        self.x = x
        self.y = y
        self.sprite_slice = sprite_slice
        self.difficulty = difficulty
        self.gameScreen = gameScreen

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Checks if the image is being clicked
        image_load = pygame.image.load(self.image).convert_alpha()
        self.frame.blit(image_load, (self.x, self.y), self.sprite_slice)

        if self.x < mouse[0] < self.x + self.sprite_slice[2] and self.y < mouse[1] < self.y + self.sprite_slice[3] and \
                click[0] == 1:
            self.gameScreen.difficulty = self.difficulty  # Sets the game difficulty to the desired


# Button that changes the amount of lives
class LivesButton:
    def __init__(self, frame, x, y, sprite_slice, lives, gameScreen):
        self.frame = frame
        self.image = "images/icons.png"
        self.x = x
        self.y = y
        self.sprite_slice = sprite_slice
        self.lives = lives
        self.gameScreen = gameScreen

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Checks if the image is being clicked
        image_load = pygame.image.load(self.image).convert_alpha()
        self.frame.blit(image_load, (self.x, self.y), self.sprite_slice)

        if self.x < mouse[0] < self.x + self.sprite_slice[2] and self.y < mouse[1] < self.y + self.sprite_slice[3] and \
                click[0] == 1:
            self.gameScreen.player.lives = self.lives  # Sets the player difficulty to the desired
            self.gameScreen.reset_lives = self.lives   # Stores the last picked lives option