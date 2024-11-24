import pygame
import random
import os
from time import sleep

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arena 1: MINIMALISM!!")

# Initialize the mixer
pygame.mixer.init()

# Load BGM (Ensure your BGM file is in the same directory or provide the correct path)
bgm_file = "assets/audio/bg_theme.mp3"  # Replace with your BGM file path
pygame.mixer.music.load(bgm_file)
pygame.mixer.music.play(0)

# Load images (Ensure your images are in the same directory or provide the correct path)
image_folder = "assets/story"  # Replace with the path to your image folder
image_files = ["0.jpeg","1.png", "2.png", "3.png", "4.png", "5.png", "6.jpeg", "7.png"]

# Load the images into a list and resize them to fit the screen
images = [pygame.image.load(os.path.join(image_folder, img)) for img in image_files]
images = [pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)) for img in images]

# Set up the clock
clock = pygame.time.Clock()

# Constants
BG_COLOR = (155, 15, 210)
PLATFORM_COLOR = (255, 255, 255)
GLOW_COLOR = (200, 200, 200)
PLAYER_COLOR = (0, 200, 200)
ENEMY_COLOR = (200, 50, 50)
PLAYER_SIZE = (40, 100)
ENEMY_SIZE = (40, 60)
PLATFORM_WIDTH, PLATFORM_HEIGHT = 600, 20
GRAVITY = 0.8
PLAYER_ATTACK_COOLDOWN = 250
PLAYER_SPEED = 5
PLAYER_JUMP = 15
DODGE_DISTANCE = 75
DODGE_COOLDOWN = 750
POWER_ATTACK_COOLDOWN = 3000
POWER_ATTACK_RADIUS = 100  # Radius of the power attack
POWER_ATTACK_DAMAGE = 40
POWER_ATTACK_HEALTH_COST = 5
SHIELD_DURATION = 3000
SHIELD_STRENGTH = 50
SHIELD_COOLDOWN = 5000

IDLE = "idle"
MOVE = "move"
JUMP = "jump"
ATTACK = "attack"
HURT = "hurt"
DEAD = "dead"
KAME = "kame"

FRAME_WIDTH = 128
FRAME_HEIGHT = 128
ANIMATION_SPEED = 100
IDLE_FRAMES = 7

font = pygame.font.SysFont("Arial", 35)

# Platform
platform_rect = pygame.Rect((SCREEN_WIDTH - PLATFORM_WIDTH) // 2, SCREEN_HEIGHT - 10, PLATFORM_WIDTH, PLATFORM_HEIGHT)

# Button settings
button_width, button_height = 75, 50
button_color = (0, 128, 255)
button_text_color = (255, 255, 255)
button_font = pygame.font.SysFont(None, 36)
button_text = button_font.render("Next", True, button_text_color)
button_rect = pygame.Rect(SCREEN_WIDTH - button_width - 20, SCREEN_HEIGHT - button_height - 20, button_width, button_height)

# Classes
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (20, 20, 20)
PLATFORM_COLOR = (2, 3, 28)
PLAYER_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)
GRAVITY = 1

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Clone Battle - Level 4")
clock = pygame.time.Clock()

# Platform
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 1000
platform_rect = pygame.Rect((SCREEN_WIDTH - PLATFORM_WIDTH) // 2, SCREEN_HEIGHT - 10, PLATFORM_WIDTH,
                            PLATFORM_HEIGHT)
background_image = pygame.transform.scale(
    pygame.image.load("assets/bg/4.png"),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# Player Class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(150, SCREEN_HEIGHT - 150, 50, 50)  # Player's size and position
        self.color = PLAYER_COLOR
        self.speed = 5
        self.is_jumping = False
        self.jump_power = 15
        self.velocity = 0
        self.health = 100
        self.attacking = False
        self.attack_cooldown = 500  # 0.5 seconds
        self.last_attack_time = 0
        self.facing_right = True

        self.kamehameha_ready = True
        self.kamehameha_cooldown = 0  # 3 seconds cooldown
        self.last_kamehameha_time = 0
        self.kamehameha_beam = None

        self.state = IDLE
        self.current_frame = 0
        self.last_update_time = 0

        self.animations = {
            IDLE: self.load_animation("assets/characters/Hero/Idle.png", 7),
            MOVE: self.load_animation("assets/characters/Hero/Run.png", 10),
            JUMP: self.load_animation("assets/characters/Hero/Jump.png", 10),
            ATTACK: self.load_animation("assets/characters/Hero/Attack_1.png", 6),
            DEAD: self.load_animation("assets/characters/Hero/Dead.png", 5),
            KAME: self.load_animation("assets/characters/Hero/Attack_2.png", 4)
        }

    def load_animation(self, path, frame_count):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(frame_count):
            frame = sprite_sheet.subsurface(pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
            frames.append(frame)
        return frames

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.last_update_time = current_time

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.current_frame = 0

    def update(self, keys, enemy):

        # Jumping mechanics
        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.set_state(JUMP)
            self.is_jumping = True
            self.velocity = -self.jump_power
        if self.is_jumping:
            self.set_state(JUMP)# Simulate gravity
            self.rect.y += self.velocity
            self.velocity += GRAVITY

        # Stop jumping when hitting the ground
        if self.rect.colliderect(platform_rect):
            self.rect.bottom = platform_rect.top
            self.is_jumping = False
            self.velocity = 0


        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.facing_right = False
            self.set_state(MOVE)
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.facing_right = True
            self.set_state(MOVE)
        else:
            if not self.attacking:
                self.set_state(IDLE)
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_k] and self.kamehameha_ready:
            # Determine direction based on enemy position
            direction = 1 if enemy.rect.centerx > self.rect.centerx else -1
            self.facing_right = True if direction == 1 else False
            self.kamehameha_beam = kamehameha((self.rect.centerx, self.rect.top), direction)
            self.kamehameha_ready = False
            self.last_kamehameha_time = current_time

        if not self.kamehameha_ready and current_time - self.last_kamehameha_time > self.kamehameha_cooldown:
            self.kamehameha_ready = True


        if self.kamehameha_beam:
            if not self.kamehameha_beam.update():
                self.kamehameha_beam = None

        # Attack mechanic
        if keys[pygame.K_z]:
            current_time = pygame.time.get_ticks()
            if not self.attacking and current_time - self.last_attack_time > self.attack_cooldown:
                self.attacking = True
                self.set_state(ATTACK)
                self.last_attack_time = current_time
                print("Player attacked!")

        self.update_animation()
        # Reset attack state after cooldown
        if pygame.time.get_ticks() - self.last_attack_time > self.attack_cooldown:
            self.attacking = False

    def draw(self, surface):
        current_image = self.animations[self.state][self.current_frame]
        pygame.transform.scale(current_image, (100, 100))
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        corrected_x = self.rect.centerx - FRAME_WIDTH // 2
        corrected_y = self.rect.centery - FRAME_HEIGHT // 2 - 40

        surface.blit(current_image, (corrected_x, corrected_y))

        health_bar = pygame.Rect(self.rect.x - (self.health / 2) + (self.rect.width / 2), self.rect.y - 30, self.health,
                                 5)
        pygame.draw.rect(surface, (0, 255, 0), health_bar)

        if self.kamehameha_beam:
            self.kamehameha_beam.draw(surface)
    def check_kamehameha_collision(self, enemy):
        if self.kamehameha_beam and self.kamehameha_beam.rect.colliderect(enemy.rect):
            enemy.health -= 20
            print(f"Enemy hit by Kamehameha! Health: {enemy.health}")
            self.kamehameha_beam = None
    def attack(self, enemy):
        if self.attacking and self.rect.colliderect(enemy.rect):
            enemy.health -= 1
            print(f"Enemy hit! Health: {enemy.health}")

    def check_collision_with_projectiles(self, projectiles):
        for projectile in projectiles[:]:
            if self.rect.colliderect(projectile.rect):
                self.health -= projectile.damage
                print(f"Player hit! Health: {self.health}")
                projectiles.remove(projectile)

class kamehameha:
    def __init__(self, start_pos, direction):
        self.rect = pygame.Rect(start_pos[0], start_pos[1], 100, 20)  # Width and height of the beam
        self.color = (0, 0, 255)  # Blue color
        self.direction = direction  # 1 for right, -1 for left
        self.speed = 10
        self.lifetime = 1000  # Lifetime in milliseconds
        self.start_time = pygame.time.get_ticks()

    def update(self):
        """Move the Kamehameha beam across the screen."""
        self.rect.x += self.speed * self.direction
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.lifetime:  # Remove the Kamehameha after its lifetime expires
            return False  # Indicates the beam should be removed
        return True

    def draw(self, surface):
        """Draw the Kamehameha beam on the screen."""
        pygame.draw.rect(surface, self.color, self.rect)


class Projectile:
    def __init__(self, x, y, direction, speed=7, damage=10):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = (255, 200, 0)
        self.speed = speed
        self.direction = direction
        self.damage = damage
        self.lifespan = 3000
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speed * self.direction

    def is_expired(self):

        return pygame.time.get_ticks() - self.spawn_time > self.lifespan

    def draw(self, surface):

        pygame.draw.rect(surface, self.color, self.rect)

class Level4Clone:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = ENEMY_COLOR
        self.health = 160
        self.max_health = 160
        self.regen_rate = 10
        self.health_regen_cooldown = 12000
        self.last_regen_time = pygame.time.get_ticks()
        self.speed = 3
        self.is_jumping = False
        self.velocity = 0
        self.teleport_cooldown = 5000
        self.last_teleport_time = pygame.time.get_ticks()
        self.teleporting = False
        self.teleport_effect_timer = 0
        self.projectiles = []
        self.shoot_cooldown = 1500  # 1.5 seconds between shots
        self.last_shoot_time = pygame.time.get_ticks()

        self.facing_right = True
        self.state = IDLE
        self.current_frame = 0
        self.last_update_time = 0

        self.animations = {
            IDLE: self.load_animation("assets/characters/Hero/Idle.png", 7),
            MOVE: self.load_animation("assets/characters/Hero/Run.png", 10),
            JUMP: self.load_animation("assets/characters/Hero/Jump.png", 10),
            ATTACK: self.load_animation("assets/characters/Hero/Attack_1.png", 6),
            HURT: self.load_animation("assets/characters/Hero/Hurt.png", 4),
            DEAD: self.load_animation("assets/characters/Hero/Dead.png", 5),
        }

    def load_animation(self, path, frame_count):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(frame_count):
            frame = sprite_sheet.subsurface(pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
            frames.append(frame)
        return frames

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.last_update_time = current_time

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.current_frame = 0


    def shoot(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time > self.shoot_cooldown:
            self.last_shoot_time = current_time

            # Determine shooting direction
            direction = 1 if player.rect.x > self.rect.x else -1

            # Create a projectile
            projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
            self.projectiles.append(projectile)
            print("Clone fired a projectile!")


    def regen_health(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_regen_time > self.health_regen_cooldown:
            self.last_regen_time = current_time
            self.health += self.regen_rate
            self.health = min(self.health, self.max_health)
            print(f"Clone regenerated health: {self.health}/{self.max_health}")

    def teleport(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time > self.teleport_cooldown:
            self.last_teleport_time = current_time
            self.teleporting = True
            self.teleport_effect_timer = pygame.time.get_ticks()

            # Play teleportation sound
            teleport_sound = pygame.mixer.Sound("assets/audio/teleport.wav")  # Add your teleport sound file
            teleport_sound.play()

            # Flash effect: Set color to white briefly
            self.color = (32, 255, 30)


            offset_x = random.choice([-150, 150])
            offset_y = random.choice([-100, 50])
            new_x = player.rect.x + offset_x
            new_y = player.rect.y + offset_y


            self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, new_x))
            self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, new_y))

            print(f"Clone teleported to ({self.rect.x}, {self.rect.y})!")

    def update(self, player):

        if self.teleporting:
            current_time = pygame.time.get_ticks()
            if current_time - self.teleport_effect_timer > 300:
                self.teleporting = False
                self.color = ENEMY_COLOR


        self.teleport(player)
        self.regen_health()
        self.shoot(player)

        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.is_expired():
                self.projectiles.remove(projectile)

        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
            self.set_state(MOVE)
            self.facing_right = True
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed
            self.set_state(MOVE)
            self.facing_right = False

        if self.is_jumping:
            self.rect.y += self.velocity
            self.velocity += GRAVITY


        if self.rect.colliderect(platform_rect):
            self.rect.bottom = platform_rect.top
            self.is_jumping = False
            self.velocity = 0

        # Jump occasionally if too close to the player
        if abs(self.rect.x - player.rect.x) < 100 and not self.is_jumping:
            self.is_jumping = True
            self.velocity = -10

    def draw(self, surface):
        current_image = self.animations[self.state][self.current_frame]
        pygame.transform.scale(current_image, (100, 100))
        if not self.facing_right:
            current_image = pygame.transform.flip(current_image, True, False)
        corrected_x = self.rect.centerx - FRAME_WIDTH // 2
        corrected_y = self.rect.centery - FRAME_HEIGHT // 2 - 40

        surface.blit(current_image, (corrected_x, corrected_y))
        health_bar = pygame.Rect(self.rect.x - (self.health / 2) + (self.rect.width / 2), self.rect.y - 30, self.health,
                                 5)
        pygame.draw.rect(surface, (255, 0, 0), health_bar)

        for projectile in self.projectiles:
            projectile.draw(surface)



def game():
    player = Player()
    enemy = Level4Clone(400, SCREEN_HEIGHT - 150)

    running = True
    while running:
        screen.fill(BG_COLOR)
        screen.blit(background_image, (0,0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        keys = pygame.key.get_pressed()


        player.update(keys, enemy)
        enemy.update(player)
        player.check_collision_with_projectiles(enemy.projectiles)
        player.attack(enemy)


        player.check_kamehameha_collision(enemy)

        # Draw platform, player, and clone
        pygame.draw.rect(screen, PLATFORM_COLOR, platform_rect)
        player.draw(screen)
        enemy.draw(screen)

        # Check win/lose conditions
        if enemy.health <= 0:
            text = font.render("Congratulations on succesfully killing yourself!", True, (231, 41, 41), 2)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_rect)

            running = False
        if player.health <= 0:
            text = font.render("Congratulations on succesfully getting killed  by yourself!", True, (231, 41, 41),2)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_rect)

            running = False

        pygame.display.flip()
        clock.tick(60)

state_story = False
image_index = 0

def show_slideshow():
    global image_index, state_story
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos) and image_index < len(images) - 1:
                    image_index += 1
                else:
                    state_story = True
                    running = False

        # Display the current image
        screen.blit(images[image_index], (0, 0))

        # Draw the button
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

# Main Game Loop
def main():
    show_slideshow()
    game()
    sleep(5)



if __name__ == "__main__":
    main()
    pygame.quit()