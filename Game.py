"""
Space Jump

Python 3.7.2
PyGame 1.9.4

Game File
"""

# Imports
from Screens import *

# Initializing PyGame
pygame.init()

# ----- Player -----
class Player:
    def __init__(self, x, y):
        self.spriteSheet = pygame.image.load("images/player_sprite.png")

        # Standing Sprite
        self.spriteSheet.set_clip(13, 10, 104, 100)
        self.standing = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        self.standing = pygame.transform.scale(self.standing, (25, 25))
        self.standing.set_colorkey((255, 255, 255))

        # Walking Sprites
        self.spriteSheet.set_clip(14, 161, 93, 99)
        walking1 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        walking1 = pygame.transform.scale(walking1, (25, 25))
        walking1.set_colorkey((255, 255, 255))

        self.spriteSheet.set_clip(127, 161, 114, 102)
        walking2 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        walking2 = pygame.transform.scale(walking2, (25, 25))
        walking2.set_colorkey((255, 255, 255))

        self.spriteSheet.set_clip(251, 163, 134, 100)
        walking3 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        walking3 = pygame.transform.scale(walking3, (25, 25))
        walking3.set_colorkey((255, 255, 255))

        self.spriteSheet.set_clip(397, 164, 111, 104)
        walking4 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        walking4 = pygame.transform.scale(walking4, (25, 25))
        walking4.set_colorkey((255, 255, 255))

        self.walking = [walking1, walking2, walking3, walking4]

        # Jumping Sprites
        self.spriteSheet.set_clip(45, 318, 110, 118)
        self.jumping1 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        self.jumping1 = pygame.transform.scale(self.jumping1, (25, 25))
        self.jumping1.set_colorkey((255, 255, 255))

        self.spriteSheet.set_clip(205, 321, 98, 113)
        self.jumping2 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert()
        self.jumping2 = pygame.transform.scale(self.jumping2, (25, 25))
        self.jumping2.set_colorkey((255, 255, 255))

        # Settings
        self.sprite = self.standing
        self.sprite_index = -1
        self.animTime = time.time()
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (x, y)
        self.action = "standing"
        self.direction = "right"
        self.falling = True
        self.jump = 0
        self.collide_platform = True   # Indicates if the player is standing on a platform
        self.collide_ladder = False    # Indicates if the player is colliding with a ladder
        self.lives = 3

    # Updates the player movement and its sprites
    def update(self):
        # Movement
        if self.action == "standing":
            if self.direction == "left":
                self.sprite = self.standing
                self.sprite = pygame.transform.flip(self.standing, True, False).copy()
            elif self.direction == "right":
                self.sprite = self.standing.copy()

        elif self.action == "walking":
            if self.direction == "left":
                self.rect.left -= 7
                self.sprite = self.get_sprite(self.walking)
                self.sprite = pygame.transform.flip(self.sprite, True, False).copy()
                if self.rect.left < 0:
                    self.rect.left = 0

            elif self.direction == "right":
                self.rect.left += 7
                self.sprite = self.get_sprite(self.walking).copy()
                if self.rect.right > 1000:
                    self.rect.right = 1000

            elif self.direction == "up" and self.collide_ladder:
                self.falling = False
                self.rect.top -= 3
                self.sprite = self.standing.copy()

            elif self.direction == "down" and self.collide_ladder and not self.collide_platform:
                self.falling = False
                self.rect.top += 3
                self.sprite = self.standing.copy()

        # Gravity and Jump
        if self.falling and self.jump <= 0:
            self.rect.top += 5
            self.sprite = self.jumping2.copy()
        elif self.jump > 0:
            self.rect.top -= 3
            self.jump -= 5
            if self.direction == "right":
                self.sprite = self.jumping1.copy()
            elif self.direction == "left":
                self.sprite = self.jumping1
                self.sprite = pygame.transform.flip(self.sprite, True, False).copy()

    # Draws a player sprite depending on the action and direction
    def draw(self, frame):
        if self.action == "standing":
            frame.blit(self.sprite, (self.rect.left, self.rect.top))
        elif self.action == "walking":
            if self.direction == "left":
                frame.blit(self.sprite, (self.rect.left, self.rect.top))
            elif self.direction == "right":
                frame.blit(self.sprite, (self.rect.left, self.rect.top))
            elif self.direction == "up":
                frame.blit(self.sprite, (self.rect.left, self.rect.top))
            elif self.direction == "down":
                frame.blit(self.sprite, (self.rect.left, self.rect.top))

    # Returns one element to be displayed from a list of sprites
    def get_sprite(self, sprites):
        if time.time() - self.animTime >= 0.15:
            self.sprite_index += 1
            self.animTime = time.time()    # Makes the animation slower
            if self.sprite_index >= (len(sprites)):
                self.sprite_index = 0
        return sprites[self.sprite_index]


# ----- Enemy -----
class Enemy:
    def __init__(self, x, y, width, height):
        self.sprite_sheet = pygame.image.load("images/enemies_spritesheet.png")

        # Flying Sprites
        self.sprite_sheet.set_clip((0, 0, 76, 32))
        self.flying1 = self.sprite_sheet.subsurface(self.sprite_sheet.get_clip()).convert_alpha()
        self.flying1 = pygame.transform.scale(self.flying1, (16, 16))

        self.sprite_sheet.set_clip((0, 32, 72, 38))
        self.flying2 = self.sprite_sheet.subsurface(self.sprite_sheet.get_clip()).convert_alpha()
        self.flying2 = pygame.transform.scale(self.flying2, (16, 16))

        self.flying = [self.flying1, self.flying2]

        # Settings
        self.sprite = self.flying1
        self.sprite_index = -1
        self.rect = pygame.Rect(x, y, width, height)
        self.height = height

        self.action = "flying"
        self.direction = "left"
        self.falling = True
        self.jumped = False   # Indicates if the player already jumped over the enemy
        self.collide_platform = True   # Indicates if the enemy is standing on a platform
        self.on_top_ladder = True      # Indicates if the enemy is standing on a ladder

        self.enemyTime = time.time()

    # Updates the enemy's movement
    def update(self):
        if self.action == "flying":
            if self.direction == "right":
                self.rect.left += 5
                self.sprite = self.get_sprite(self.flying)
                self.sprite = pygame.transform.flip(self.sprite, True, False).copy()
            elif self.direction == "left":
                self.rect.left -= 5
                self.sprite = self.get_sprite(self.flying).copy()

        if self.falling:
            self.action = "standing"
            self.rect.top += 3
            self.sprite = self.flying1.copy()

    # Draws an enemy sprite depending on the action and direction
    def draw(self, frame):
         if self.action == "standing":
            frame.blit(self.sprite, (self.rect.left,  self.rect.bottom - 16))
         elif self.action == "flying":
            if self.direction == "left":
                frame.blit(self.sprite, (self.rect.left,  self.rect.bottom - 16))
            elif self.direction == "right":
                frame.blit(self.sprite, (self.rect.left,  self.rect.bottom - 16))

    # Returns one element to be displayed from a list of sprites
    def get_sprite(self, sprites):
        if time.time() - self.enemyTime >= 0.25:
            self.sprite_index += 1
            self.enemyTime = time.time()   # Makes the animation slower
            if self.sprite_index >= (len(sprites)):
                self.sprite_index = 0
        return sprites[self.sprite_index]


# ----- Platforms -----
class Platform:
    def __init__(self, x, y, width, height):
        # Settings
        self.rect = pygame.Rect(x, y, width, height)
        self.walked = False  # Indicates if the player already stepped on the platform

    # Draws the platform
    def draw(self, frame):
        pygame.draw.rect(frame, (0, 153, 76), self.rect)


# ----- Ladders -----
class Ladder:
    def __init__(self, x, y, width, height):
        self.y = y
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    # Draws the ladder
    def draw(self, frame):
        pygame.draw.rect(frame, (139, 119, 101), self.rect)


# ----- Game Screen -----
class GameScreen:
    def __init__(self, frame, flags, scores_ints):
        self.frame = frame
        self.flags = flags

        self.player = Player(0, 521)  # Creates the player
        self.score = -50              # Sets the inicial score

        self.enemies = []             # Creates the enemy list

        self.reset_lives = 3          # Indicates the lives chosen by the user

        self.platforms = []           # Creates the platforms list

        self.ladders = []             # Creates the ladders list

        self.difficulty = "easy"      # Sets the default difficulty
        self.map_called = False       # Indicates if the method map has been already called
        self.last_time = time.time()

        self.scores_ints = scores_ints

        # Boss
        self.boss = pygame.image.load("images/enemies_spritesheet.png")

        # Flying
        self.boss.set_clip((0, 0, 76, 32))
        flying1 = self.boss.subsurface(self.boss.get_clip()).convert_alpha()

        self.boss.set_clip((0, 32, 72, 38))
        flying2 = self.boss.subsurface(self.boss.get_clip()).convert_alpha()

        self.flying = [flying1, flying2]

        # Boss Settings
        self.boss_sprite = flying1
        self.boss_sprite_index = -1
        self.boss_rect = self.boss_sprite.get_rect()
        self.bossTime = time.time()

        # Chest
        self.chest = pygame.image.load("images/chest.png").convert_alpha()
        self.chest = pygame.transform.scale(self.chest, (64, 64))
        self.chest_rect = self.chest.get_rect()

    # Generates the leveles automatically
    def map(self):
        y = 0   # y coordinate
        n = 0   # counter
        k = 0   # times to repeat

        self.platforms = [Platform(0, 546, 1000, 16), Platform(0, 471, 699, 16), Platform(731, 471, 219, 16),
                          Platform(50, 396, 219, 16), Platform(301, 396, 699, 16)]
        self.ladders = [Ladder(700, 471, 30, 75), Ladder(270, 396, 30, 75)]

        if self.difficulty == "medium":
            k = 2
        elif self.difficulty == "hard":
            k = 4

        while n < k:
            if n % 2 == 0:
                self.platforms.append(Platform(0, 396 - 75 + y, 699, 16))
                self.platforms.append(Platform(731, 396 - 75 + y, 219, 16))
                self.ladders.append(Ladder(700, 471 - 150 + y, 30, 75))
            else:
                self.platforms.append(Platform(50, 396 - 75 + y, 219, 16))
                self.platforms.append(Platform(301, 396 - 75 + y, 699, 16))
                self.ladders.append(Ladder(270, 396 - 75 + y, 30, 75))
            y -= 75
            n += 1

        self.map_called = True  # This way the main loop will stop calling map()

    # Resets the game
    def restart(self):
        self.player.rect.topleft = (0, 521)    # Relocates the player
        self.player.lives = self.reset_lives   # Set lives as the last option picked

        self.platforms.clear()    # Removes all platforms
        self.ladders.clear()      # Removes all ladders
        self.enemies.clear()      # Removes all enemies
        self.score = -50          # Resets the score

        self.map_called = False   # So we can call it again and generate the map
        self.last_time = time.time()


    # Handles the player and enemies movements and collisions, the boss animation and the chest
    def update(self):
        # Boss
        self.boss_sprite = self.get_sprite(self.flying).copy()

        # Player
        self.player.falling = True
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect) and self.player.rect.bottom <= platform.rect.top + 5:
                self.player.falling = False  # Keeps the player from falling through the platforms
                self.player.collide_platform = True
                if platform.walked == False:
                    self.score += 50         # Adds to the score if the player reached a new platform
                    platform.walked = True   # Lets the game know the player already stepped on the platform
                break
            else:
                self.player.collide_platform = False


        for ladder in self.ladders:
            if self.player.rect.colliderect(ladder.rect):
                self.player.collide_ladder = True  # Keeps the player from falling through the ladders
                self.player.falling = False
                break
            else:
                self.player.collide_ladder = False

        # Enemy

        # Generates enemies after a certain time
        if time.time() - self.last_time >= 3:
            if self.difficulty == "hard":
                self.enemies.append(Enemy(930, 20, 16, 75))   # Positions the enemy according to the level
            elif self.difficulty == "medium":
                self.enemies.append(Enemy(930, 170, 16, 75))
            else:
                self.enemies.append(Enemy(930, 325, 16, 65))
            self.last_time = time.time()
            
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.platforms[0].rect):
                self.enemies.remove(enemy)  # Removes the enemy if it reached the lowest platform
                break

            enemy.falling = True
            for platform in self.platforms:
                if enemy.rect.colliderect(platform.rect) and enemy.rect.bottom <= platform.rect.top + 5:
                    enemy.action = "flying"
                    enemy.falling = False    # Keeps the enemy from falling through the platforms
                    enemy.collide_platform = True
                    break
                else:
                    enemy.collide_platform = False

                if enemy.rect.right >= 984:   # Makes the enemy change direction upon reaching a wall
                    enemy.direction = "left"
                        
                elif enemy.rect.left <= 0:    # Makes the enemy change direction upon reaching a wall
                    enemy.direction = "right"

            for ladder in self.ladders:
                if enemy.rect.colliderect(ladder.rect) and enemy.rect.bottom <= ladder.rect.top + 10:
                    enemy.action = "flying"
                    enemy.falling = False   # Keeps the enemy from falling through the ladders
                    enemy.on_top_ladder = True
                    break
                else:
                    enemy.on_top_ladder = False

            enemy.update()   # Updates the enemy

        # Player update
        self.player.update()  # Updates the player

        # Player and Enemy Collision
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.rect.bottom >= enemy.rect.top + enemy.height - 16:
                    self.player.lives -= 1   # Removes a life from the player if it collides with an enemy
                    self.player.rect.topleft = (0, 521)  # Returns the player to the beginning
                else:
                    if not enemy.jumped:
                        enemy.jumped = True  # Lets the game know the player already jumped over that enemy
                        self.score += 50     # Adds to the score

            if self.player.lives == 0:       # Ends the game if the player loses all of his lives
                flags["Game"] = False
                flags["Game Over"] = True
                self.restart()               # Resets the game

        # Chest Collision
            if self.player.rect.colliderect(self.chest_rect):
                self.scores_ints.append(self.score)   # Adds the player's score to a list
                self.scores_ints.sort()
                self.scores_ints.reverse()
                self.scores_ints = self.scores_ints[:3]  # Gets the three highest scores until that moement

                flags["Game"] = False
                flags["Win"] = True          # The player wins upon touching the chest
                self.restart()       # # Resets the game

    # Draws backgroung image, boss, chest, score, lives, platforms, enemies, ladders and t player
    def draw(self):
        bg = pygame.image.load("images/game_bg.png").convert()
        self.frame.blit(bg, (0, 0))

        if self.difficulty == "easy":
            self.frame.blit(self.boss_sprite, (920, 350))
            self.frame.blit(self.chest, (850, 340))
            self.chest_rect = pygame.Rect(850, 340, 64, 64)
        elif self.difficulty == "medium":
            self.frame.blit(self.boss_sprite, (920, 200))
            self.frame.blit(self.chest, (850, 190))
            self.chest_rect = pygame.Rect(850, 190, 64, 64)
        else:
            self.frame.blit(self.boss_sprite, (920, 50))
            self.frame.blit(self.chest, (850, 40))
            self.chest_rect = pygame.Rect(850, 40, 64, 64)

        display_text(self.frame, "Score: %s" % self.score, 30, 5, 0)
        display_text(self.frame, "Lives: %s" % self.player.lives, 30, 890, 0)

        # Platforms
        for platform in self.platforms:
            platform.draw(self.frame)
            
        # Ladders
        for ladder in self.ladders:
            ladder.draw(self.frame)

        # Enemies
        for enemy in self.enemies:
            enemy.draw(self.frame)

        # Player
        self.player.draw(self.frame)

    # Returns one element to be displayed from a list of sprites
    def get_sprite(self, sprites):
        if time.time() - self.bossTime >= 0.25:
            self.boss_sprite_index += 1
            self.bossTime = time.time()
            if self.boss_sprite_index >= (len(sprites)):
                self.boss_sprite_index = 0
        return sprites[self.boss_sprite_index]

# ----- Events -----
    # Handles all of the in-game events
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.player.action = "walking"
                self.player.direction = "left"
                
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.player.action = "walking"
                self.player.direction = "right"

            elif event.key == pygame.K_SPACE and self.player.jump <= 0 and not self.player.falling:
                self.player.jump = 75

            elif event.key == pygame.K_UP or event.key == pygame.K_w and self.player.collide_ladder:
                self.player.action = "walking"
                self.player.direction = "up"
                self.player.falling = False

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s and self.player.collide_ladder:
                self.player.action = "walking"
                self.player.direction = "down"
                self.player.falling = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.player.action = "standing"
                self.player.direction = "left"
                
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.player.action = "standing"
                self.player.direction = "right"

            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.player.action = "standing"
                self.player.direction = "up"

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.player.action = "standing"
                self.player.direction = "down"

# Quit
pygame.quit()
