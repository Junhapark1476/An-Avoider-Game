import pygame, sys, random

# Test if two sprite masks overlap
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return bool(overlap)

# Base Sprite Class
class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)

# Player Class
class Player(Sprite):
    def __init__(self, image):
        super().__init__(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position

# Enemy Class
class Enemy(Sprite):
    def __init__(self, image, width, height):
        super().__init__(image)
        self.rectangle.center = (
            random.randint(0, width - self.rectangle.width),
            random.randint(0, height - self.rectangle.height)
        )
        self.speed = [
            random.choice([-1, 1]) * random.randint(2, 5),
            random.choice([-1, 1]) * random.randint(2, 5)
        ]

    def move(self):
        self.rectangle.move_ip(self.speed[0], self.speed[1])

    def bounce(self, width, height):
        if self.rectangle.left < 0 or self.rectangle.right > width:
            self.speed[0] *= -1
        if self.rectangle.top < 0 or self.rectangle.bottom > height:
            self.speed[1] *= -1

# PlatformEnemy Class
class PlatformEnemy(Enemy):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.speed[1] = 0  # vy = 0 (horizontal only)

# PowerUp Class
class PowerUp(Sprite):
    def __init__(self, image, width, height):
        super().__init__(image)
        self.rectangle.center = (
            random.randint(0, width - self.rectangle.width),
            random.randint(0, height - self.rectangle.height)
        )

# RotatingPowerUp Class
class RotatingPowerUp(PowerUp):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.angle = 0
        self.original_image = image

    def draw(self, screen):
        self.angle += 3  # Rotate 3 degrees per frame
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        center = self.rectangle.center
        self.image = rotated_image
        self.rectangle = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)
        super().draw(screen)

# Main game function
def main():
    pygame.init()
    pygame.mixer.init()
    start_ticks = pygame.time.get_ticks()

    pygame.mixer.music.load("game_bgm_1.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    myfont = pygame.font.SysFont('monospace', 24)

    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))

    # Load images
    enemy_image = pygame.transform.smoothscale(pygame.image.load("picture3.png").convert_alpha(), (150, 150))
    player_image = pygame.transform.smoothscale(pygame.image.load("picture1.png").convert_alpha(), (300, 300))
    powerup_image = pygame.transform.smoothscale(pygame.image.load("picture2.png").convert_alpha(), (80, 80))
    rotating_powerup_image = pygame.transform.smoothscale(pygame.image.load("picture4.png").convert_alpha(), (80, 80))

    # Create sprites
    enemy_sprites = []
    for _ in range(7):
        enemy_sprites.append(Enemy(enemy_image, width, height))
    for _ in range(3):
        enemy_sprites.append(PlatformEnemy(enemy_image, width, height))

    player_sprite = Player(player_image)
    powerups = []

    life = 3
    is_playing = True

    while is_playing and life > 0:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds >= 60:
            is_playing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False

        # Player follows mouse
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        # Check collisions
        for enemy in enemy_sprites:
            if player_sprite.is_colliding(enemy):
                life -= 0.1

        for powerup in powerups:
            if player_sprite.is_colliding(powerup):
                if isinstance(powerup, RotatingPowerUp):
                    life += 1  # Rotating powerup gives more
                else:
                    life += 0.5

        # Remove collected powerups
        powerups = [p for p in powerups if not player_sprite.is_colliding(p)]

        # Move and bounce enemies
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width, height)

        # Randomly spawn PowerUps
        if random.random() < 0.008:
            if random.random() < 0.5:
                powerups.append(PowerUp(powerup_image, width, height))
            else:
                powerups.append(RotatingPowerUp(rotating_powerup_image, width, height))

        # Draw everything
        screen.fill((0, 100, 50))

        for enemy in enemy_sprites:
            enemy.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)
        player_sprite.draw(screen)

        # Draw life and time
        life_text = "Life: " + str('%.1f' % life)
        life_banner = myfont.render(life_text, True, (255, 255, 0))
        screen.blit(life_banner, (20, 20))

        remaining_time = max(0, 60 - int(seconds))
        time_text = "Time: " + str(remaining_time)
        time_banner = myfont.render(time_text, True, (255, 255, 255))
        screen.blit(time_banner, (20, 50))

        pygame.display.update()
        pygame.time.wait(20)

    pygame.time.wait(2000)
    pygame.mixer.music.stop()

    # End screen
    screen.fill((0, 0, 0))
    if life > 0:
        message = myfont.render("Time's up!", True, (255, 255, 255))
    else:
        message = myfont.render("Game Over you die!", True, (255, 255, 255))
    screen.blit(message, (width // 2 - message.get_width() // 2, height // 2))
    pygame.display.update()
    pygame.time.wait(3000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


