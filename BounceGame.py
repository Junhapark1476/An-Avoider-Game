import pygame, sys, math, random

# Test if two sprite masks overlap
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    if overlap:
        return True
    else:
        return False

# A basic Sprite class that can draw itself, move, and test collisions. Basically the same as 
# the Character example from class.
class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)


class Enemy:
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

        # Add code to
        # 1. Set the rectangle center to a random x and y based
        #    on the screen width and height
        # 2. Set a speed instance variable that holds a tuple (vx, vy)
        #    which specifies how much the rectangle moves each time.
        #    vx means "velocity in x". Make the vx and vy random (with
        #    possible negative and positive values. Experiment so the 
        #    speeds are not too fast.
        self.rectangle.center = (
            random.randint(0, width - self.rectangle.width),
            random.randint(0, height - self.rectangle.height)
        )
        vx = random.choice([-1, 1]) * random.randint(2, 5)
        vy = random.choice([-1, 1]) * random.randint(2, 5)
        self.speed = [vx, vy]



    def move(self):
        self.rectangle.move_ip(self.speed[0], self.speed[1])
        print("need to implement move!")
        # Add code to move the rectangle instance variable in x by
        # the speed vx and in y by speed vy. The vx and vy are the
        # components of the speed instance variable tuple.
        # A useful method of rectangle is pygame's move_ip method.
        # Research how to use it for this task.

    def bounce(self, width, height):
        if self.rectangle.left < 0 or self.rectangle.right > width:
            self.speed[0] *= -1
        if self.rectangle.top < 0 or self.rectangle.bottom > height:
            self.speed[1] *= -1
        print("need to implement bounce!")
        # This method makes the enemy bounce off of the top/left/right/bottom
        # of the screen. For example, if you want to check if the object is
        # hitting the left side, you can test
        # if self.rectangle.left < 0:
        # The rectangle.left tests the left side of the rectangle. You will
        # want to use .right .top .bottom for the other sides.
        # The height and width parameters gives the screen boundaries.
        # If a hit of the edge of the screen is detected on the top or bottom
        # you want to negate (multiply by -1) the vy component of the speed instance
        # variable. If a hit is detected on the left or right of the screen, you
        # want to negate the vx component of the speed.
        # Make sure the speed instance variable is updated as needed.

    def draw(self, screen):
        # Same draw as Sprite
        screen.blit(self.image, self.rectangle)

class PowerUp:
    def __init__(self, image, width, height):
        # Set the PowerUp position randomly like is done for the Enemy class.
        # There is no speed for this object as it does not move.
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (
            random.randint(0, width - self.rectangle.width),
            random.randint(0, height - self.rectangle.height)
        )
    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

class StrongPowerUp:
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (
            random.randint(0, width - self.rectangle.width),
            random.randint(0, height - self.rectangle.height)
        )

    def draw(self, screen):
        # Same as Sprite
        screen.blit(self.image, self.rectangle)


def main():
    # Setup pygame
    pygame.init()
    pygame.mixer.init()
    start_ticks = pygame.time.get_ticks()
    pygame.mixer.music.load("game_bgm_1.mp3")
    pygame.mixer.music.set_volume(0.3)  # sound volume (0.0 ~ 1.0)
    pygame.mixer.music.play(-1)  # infinite sound

    # Get a font for printing the lives left on the screen.
    myfont = pygame.font.SysFont('monospace', 24)

    # Define the screen
    width, height = 600, 400
    size = width, height
    screen = pygame.display.set_mode((width, height))

    # Load image assets
    # Choose your own image
    enemy = pygame.image.load("picture3.png").convert_alpha()
    # Here is an example of scaling it to fit a 50x50 pixel size.
    enemy_image = pygame.transform.smoothscale(enemy, (150, 150))

    enemy_sprites = []
    # Make some number of enemies that will bounce around the screen.
    # Make a new Enemy instance each loop and add it to enemy_sprites.
    for _ in range(10):
        enemy_sprites.append(Enemy(enemy_image, width, height))

    # This is the character you control. Choose your image.
    player = pygame.image.load("picture1.png").convert_alpha()
    player_image = pygame.transform.smoothscale(player, (300, 300))
    player_sprite = Sprite(player_image)
    life = 3

    # This is the powerup image. Choose your image.
    powerup = pygame.image.load("picture2.png").convert_alpha()
    powerup_image = pygame.transform.smoothscale(powerup, (80, 80))
    # Start with an empty list of powerups and add them as the game runs.
    powerups = []

    powerup2 = pygame.image.load("picture4.png").convert_alpha()
    powerup2_image = pygame.transform.smoothscale(powerup2, (80, 80))
    strong_powerups = []

    # Main part of the game
    is_playing = True
    # while loop
    while is_playing and life > 0: # while is_playing is True, repeat
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # 🔸 Time elapsed (seconds)
        if seconds >= 60:
            is_playing = False  # 🔸 Game over after 60 seconds
    # Modify the loop to stop when life is <= to 0.

        # Check for events
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == pygame.QUIT:
                is_playing = False

        # Make the player follow the mouse
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        # Loop over the enemy sprites. If the player sprite is
        # colliding with an enemy, deduct from the life variable.

        for enemy in enemy_sprites:
            if player_sprite.is_colliding(enemy):
                life -= 0.1
            # A player is likely to overlap an enemy for a few iterations
        # of the game loop - experiment to find a small value to deduct that
        # makes the game challenging but not frustrating.

        # Loop over the powerups. If the player sprite is colliding, add
        # 1 to the life.
        for powerup in powerups:
            if player_sprite.is_colliding(powerup):
                life += 0.5
        # Make a list comprehension that removes powerups that are colliding with
        powerups = [p for p in powerups if not player_sprite.is_colliding(p)]
        # the player sprite.

        for strong in strong_powerups:
            if player_sprite.is_colliding(strong):
                life += 1
        strong_powerups = [s for s in strong_powerups if not player_sprite.is_colliding(s)]
        # Loop over the enemy_sprites. Each enemy should call move and bounce.
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width, height)
        # Choose a random number. Use the random number to decide to add a new
        # powerup to the powerups list. Experiment to make them appear not too
        # often, so the game is challenging.
        if random.random() < 0.008:
            powerups.append(PowerUp(powerup_image, width, height))

        if random.random() < 0.002:
            strong_powerups.append(StrongPowerUp(powerup2_image, width, height))

        # Erase the screen with a background color
        screen.fill((0,100,50)) # fill the window with a color


        # Draw the characters
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)
        for strong_sprite in strong_powerups:
            strong_sprite.draw(screen)

        player_sprite.draw(screen)

        # Write the life to the screen.
        text = "Life: " + str('%.1f'%life)
        life_banner = myfont.render(text, True, (255, 255, 0))
        screen.blit(life_banner, (20, 20))


        remaining_time = max(0, 60 - int(seconds))  # Calculation of time remaining
        time_text = "Time: " + str(remaining_time)
        time_banner = myfont.render(time_text, True, (255, 255, 255))
        screen.blit(time_banner, (20, 50))


        # Bring all the changes to the screen into view
        pygame.display.update()
        # Pause for a few milliseconds
        pygame.time.wait(20)

    pygame.time.wait(2000)
    pygame.mixer.music.stop()
    if life > 0:      #Game ending
        screen.fill((0, 0, 0))
        message = myfont.render("Time's up!", True, (255, 255, 255))
        screen.blit(message, (width // 2 - message.get_width() // 2, height // 2))
        pygame.display.update()
        pygame.time.wait(3000)
    if life <= 0:
        screen.fill((0, 0, 0))
        message = myfont.render("Game Over you die!", True, (255, 255, 255))
        screen.blit(message, (width // 2 - message.get_width() // 2, height // 2))
        pygame.display.update()
        pygame.time.wait(3000)
    pygame.quit()
    sys.exit()
    # Once the game loop is done, pause, close the window and quit.
    # Pause for a few seconds

if __name__ == "__main__":
    main()
