"""
Valley Jump

Python 3.7.2
PyGame 1.9.4

Main File
"""

# Libraries
from Game import *
from Screens import *

# Settings
displayWidth = 1000
displayHeight = 562
FPS = 30

# Opens the .txt and puts each line as an element of a list
file = open("scores.txt", "r")
scores_list = file.readlines()
file.close()

# Handles the scores
scores_string = ""

for score in scores_list:
    scores_string += score

scores_string = scores_string.split("/")
scores_string = scores_string[:3]
scores_ints = []

for score in scores_string:
    scores_ints.append(int(score))

# Initializing PyGame
pygame.init()

# Music
pygame.mixer.music.load("music/mushrooms.mp3")


# # ----- Main Display -----
displayFlag = True
frame = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Valley Jump")
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

# Creates the instances of all the screens
introScreen = IntroScreen(frame, FPS, flags)
menuScreen = MenuScreen(frame, flags)
leaderboardScreen = LeaderboardScreen(frame, flags, scores_ints)
gameScreen = GameScreen(frame, flags, scores_ints)
settingsScreen = SettingsScreen(frame, flags, gameScreen)
gameOverScreen = GameOverScreen(frame, flags)
winScreen = WinScreen(frame, flags)

# Main Loop
while displayFlag:
    # Checks for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            displayFlag = False
        if flags["Game"]:
            gameScreen.events(event)

    # Checks each flag's value in the flags dictionary
    for flag, value in flags.items():
        if value == True:
            if flag == "Intro":
                introScreen.update()
                introScreen.draw()

            elif flag == "Menu":
                menuScreen.draw()

            elif flag == "Settings":
                settingsScreen.draw()

            elif flag == "Leaderboard":
                leaderboardScreen.scores_ints = gameScreen.scores_ints
                leaderboardScreen.draw()

            elif flag == "Game":
                if not gameScreen.map_called:
                    gameScreen.map()
                gameScreen.update()
                gameScreen.draw()

            elif flag == "Game Over":
                gameOverScreen.draw()

            elif flag == "Win":
                winScreen.draw()

            elif flag == "Exit":
                pygame.quit()
                quit()

    pygame.display.update()
    clock.tick(FPS)


# Updates the score
file = open("scores.txt", "w")

scores_list = gameScreen.scores_ints
scores_list = scores_list[:3]
scores_list.sort()
scores_list.reverse()

for score in scores_list:
    file.write(str(score) + "/")

file.close()


# Quit
pygame.quit()
quit()
