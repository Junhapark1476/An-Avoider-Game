# Assignment Title : BounceGame Extension by Junha Park

import pygame, sys, random

# Test for pixel-perfect collision
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
        self.speed = [random.choice([-1, 1]) * random.randint(2, 5),
                      random.choice([-1, 1]) * random.randint(2, 5)]

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
        self.speed[1] = 0  # # Set vertical speed to 0 (horizontal only)

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
        super().__init__(image, width, height)  # Call the parent class constructor to initialize the sprite
        self.angle = 0  # Initial angle for rotation
        self.original_image = image

    def draw(self, screen):
        self.angle += 3  # Rotate 3 degrees each frame
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
    enemy_sprites = [Enemy(enemy_image, width, height) for _ in range(7)]  # Regular enemies
    enemy_sprites += [PlatformEnemy(enemy_image, width, height) for _ in range(3)]  # Platform enemies
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

        # Collision checks
        for enemy in enemy_sprites:
            if player_sprite.is_colliding(enemy):
                life -= 0.1

        for powerup in powerups:
            if player_sprite.is_colliding(powerup):
                life += 1 if isinstance(powerup, RotatingPowerUp) else 0.5

        powerups = [p for p in powerups if not player_sprite.is_colliding(p)]  # Remove collected power-ups

        # Move and bounce enemies
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width, height)

        # Randomly spawn power-ups
        if random.random() < 0.008:
            powerups.append(PowerUp(powerup_image, width, height) if random.random() < 0.5 else RotatingPowerUp(rotating_powerup_image, width, height))

        # Draw everything
        screen.fill((0, 100, 50))

        for enemy in enemy_sprites:
            enemy.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)
        player_sprite.draw(screen)

        # Display life and time remaining
        life_text = f"Life: {life:.1f}"
        screen.blit(myfont.render(life_text, True, (255, 255, 0)), (20, 20))
        remaining_time = max(0, 60 - int(seconds))
        time_text = f"Time: {remaining_time}"
        screen.blit(myfont.render(time_text, True, (255, 255, 255)), (20, 50))

        pygame.display.update()
        pygame.time.wait(20)

    pygame.time.wait(2000)
    pygame.mixer.music.stop()

    # End screen
    screen.fill((0, 0, 0))
    message = myfont.render("Time's up!" if life > 0 else "Game Over you die!", True, (255, 255, 255))
    screen.blit(message, (width // 2 - message.get_width() // 2, height // 2))
    pygame.display.update()
    pygame.time.wait(3000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



