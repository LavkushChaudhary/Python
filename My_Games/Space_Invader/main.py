import pygame
import os
import time
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 700

game_window = pygame.display.set_mode((WIDTH, HEIGHT))

# Enemy spaceships
RED_SPACE_SHIP = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\pixel_ship_red_small.png')
BLUE_SPACE_SHIP = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\pixel_ship_blue_small.png')
GREEN_SPACE_SHIP = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\pixel_ship_green_small.png')
# Player spaceship
YELLOW_SPACE_SHIP = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\pixel_ship_yellow.png')

# Enemy bullets
RED_BULLET = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\pixel_bullet_red.png')
BLUE_BULLET = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\pixel_bullet_blue.png')
GREEN_BULLET = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\pixel_bullet_green.png')

# Player Bullet
YELLOW_BULLET = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\pixel_bullet_yellow.png')

# Background
BG_PATH = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\space.jpg')
BG = pygame.transform.scale(BG_PATH, (WIDTH, HEIGHT))

LOCK_SYMBOL = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\lock.jpg')
LOCK_SYMBOL = pygame.transform.scale(LOCK_SYMBOL, (50, 50))
LOCK_SYMBOL.set_alpha(255)  # Make the lock image opaque

HEALTH_PACK = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\health_pack.jpg')
HEALTH_PACK = pygame.transform.scale(HEALTH_PACK, (30, 30))

# Load and play background music
pygame.mixer.music.load(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\BackgroundMusic.mp3')
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load bullet sound
BULLET_SOUND = pygame.mixer.Sound(r'C:\Users\Scp\Desktop\Python\My_Games\Space_Invader\gunsound.mp3')

def draw_window(BG, player, player_x, player_y, bullets, player_health, health_packs):
    game_window.blit(BG, (0, 0))
    for bullet in bullets:
        game_window.blit(YELLOW_BULLET, (bullet.x, bullet.y))
    for health_pack in health_packs:
        game_window.blit(HEALTH_PACK, (health_pack.x, health_pack.y))
    game_window.blit(player, (player_x, player_y))
    draw_health_bar(player_x, player_y, player_health)
    pygame.display.update()

def draw_health_bar(x, y, health):
    pygame.draw.rect(game_window, (255, 0, 0), (x, y + YELLOW_SPACE_SHIP.get_height() + 10, YELLOW_SPACE_SHIP.get_width(), 10))
    pygame.draw.rect(game_window, (0, 255, 0), (x, y + YELLOW_SPACE_SHIP.get_height() + 10, YELLOW_SPACE_SHIP.get_width() * (health / 100), 10))

def draw_button(rect, text, locked=False):
    font = pygame.font.SysFont('comicsans', 60)
    if not locked:
        label = font.render(text, 1, (255, 255, 255))
        game_window.blit(label, (rect.x + rect.width // 2 - label.get_width() // 2, rect.y + 5))
    if locked:
        lock_rect = LOCK_SYMBOL.get_rect(center=(rect.x + rect.width // 2, rect.y + rect.height // 2))
        game_window.blit(LOCK_SYMBOL, lock_rect)

def draw_menu():
    game_window.blit(BG, (0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    title_label = font.render("Press the Start Button to Begin", 1, (255, 255, 255))
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    game_window.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 2 - 150))
    draw_button(start_button, "Start")
    draw_button(exit_button, "Exit")
    pygame.display.update()
    return start_button, exit_button

def draw_levels(unlocked_levels):
    game_window.blit(BG, (0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    title_label = font.render("Select Level", 1, (255, 255, 255))
    game_window.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 2 - 300))
    level_buttons = []
    button_width = 100
    button_height = 50
    padding = 20
    buttons_per_row = 5
    for i in range(5):
        x = WIDTH // 2 - (button_width + padding) * buttons_per_row // 2 + (button_width + padding) * (i % buttons_per_row)
        y = HEIGHT // 2 - 200 + (button_height + padding) * (i // buttons_per_row)
        level_button = pygame.Rect(x, y, button_width, button_height)
        if i + 1 <= unlocked_levels:
            draw_button(level_button, str(i + 1))
        else:
            draw_button(level_button, "", locked=True)
        level_buttons.append(level_button)
    pygame.display.update()
    return level_buttons

def draw_game_mode():
    game_window.blit(BG, (0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    title_label = font.render("Select Game Mode", 1, (255, 255, 255))
    game_window.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 2 - 300))
    level_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    draw_button(level_button, "Levels")
    pygame.display.update()
    return level_button

def game_mode_menu(unlocked_levels):
    run = True
    while run:
        level_button = draw_game_mode()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if level_button.collidepoint(mouse_pos):
                    level_menu(unlocked_levels)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    exit()
        if not pygame.display.get_init():
            run = False

def level_menu(unlocked_levels):
    run = True
    while run:
        level_buttons = draw_levels(unlocked_levels)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, level_button in enumerate(level_buttons):
                    if level_button.collidepoint(mouse_pos) and i + 1 <= unlocked_levels:
                        main(level=i + 1, unlocked_levels=unlocked_levels)
                        run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    exit()
        if not pygame.display.get_init():
            run = False

def main_menu(unlocked_levels=1):
    run = True
    while run:
        start_button, exit_button = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    game_mode_menu(unlocked_levels)
                if exit_button.collidepoint(mouse_pos):
                    run = False
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    exit()
        if not pygame.display.get_init():
            run = False

class Enemy:
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_BULLET),
        "green": (GREEN_SPACE_SHIP, GREEN_BULLET),
        "blue": (BLUE_SPACE_SHIP, BLUE_BULLET)
    }

    def __init__(self, x, y, color, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img, self.bullet_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.bullets = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for bullet in self.bullets:
            window.blit(self.bullet_img, (bullet.x, bullet.y))

    def move(self, vel):
        self.y += vel
        if self.y > 0:  # Enemy is on the screen
            self.shoot()

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = pygame.Rect(
                self.x + self.ship_img.get_width() // 2 - self.bullet_img.get_width() // 2,
                self.y + self.ship_img.get_height(),
                self.bullet_img.get_width(),
                self.bullet_img.get_height()
            )
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def move_bullets(self, vel, player_rect, player_health, level):
        self.cooldown()
        bullet_damage = {1: 2, 2: 5, 3: 10, 4: 25, 5: 50}.get(level, 2)
        for bullet in self.bullets:
            bullet.y += vel
            if bullet.y > HEIGHT:
                self.bullets.remove(bullet)
            elif bullet.colliderect(player_rect):
                player_health -= bullet_damage
                self.bullets.remove(bullet)
        return player_health

    def cooldown(self):
        if self.cool_down_counter >= 30:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

def draw_pause_menu():
    font = pygame.font.SysFont('comicsans', 60)
    title_label = font.render("Game Paused", 1, (255, 255, 255))
    game_window.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 2 - 150))
    unpause_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    draw_button(unpause_button, "Unpause")
    draw_button(menu_button, "Menu")
    pygame.display.update()
    return unpause_button, menu_button

def pause_menu():
    paused = True
    while paused:
        unpause_button, menu_button = draw_pause_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if unpause_button.collidepoint(mouse_pos):
                    paused = False
                if menu_button.collidepoint(mouse_pos):
                    main_menu()
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        if not pygame.display.get_init():
            paused = False

def draw_lives(lives):
    font = pygame.font.SysFont('comicsans', 30)
    lives_label = font.render(f"Lives: {lives}", 1, (255, 255, 255))
    game_window.blit(lives_label, (10, 10))

def draw_kills(kills):
    font = pygame.font.SysFont('comicsans', 30)
    kills_label = font.render(f"Kills: {kills}", 1, (255, 255, 255))
    game_window.blit(kills_label, (10, 40))

def draw_level(level):
    font = pygame.font.SysFont('comicsans', 30)
    level_label = font.render(f"Level: {level}", 1, (255, 255, 255))
    game_window.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

def draw_lost_menu(kills):
    font = pygame.font.SysFont('comicsans', 60)
    lost_label = font.render("You Lost!", 1, (255, 0, 0))
    kills_label = font.render(f"Total Kills: {kills}", 1, (255, 255, 255))
    game_window.blit(lost_label, (WIDTH // 2 - lost_label.get_width() // 2, HEIGHT // 2 - 150))
    game_window.blit(kills_label, (WIDTH // 2 - kills_label.get_width() // 2, HEIGHT // 2 - 100))
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    draw_button(restart_button, "Restart")
    draw_button(menu_button, "Menu")
    pygame.display.update()
    return restart_button, menu_button

def lost_menu(kills, unlocked_levels):
    lost = True
    while lost:
        restart_button, menu_button = draw_lost_menu(kills)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    main(unlocked_levels=unlocked_levels)
                    return
                if menu_button.collidepoint(mouse_pos):
                    main_menu(unlocked_levels)
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main(unlocked_levels=unlocked_levels)
                    return
                if event.key == pygame.K_m:
                    main_menu(unlocked_levels)
                    return
        if not pygame.display.get_init():
            lost = False

def draw_win_menu():
    font = pygame.font.SysFont('comicsans', 60)
    win_label = font.render("You Won!", 1, (0, 255, 0))
    game_window.blit(win_label, (WIDTH // 2 - win_label.get_width() // 2, HEIGHT // 2 - 150))
    next_level_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    draw_button(next_level_button, "Next Level")
    draw_button(menu_button, "Menu")
    pygame.display.update()
    return next_level_button, menu_button

def win_menu(level, unlocked_levels):
    won = True
    while won:
        next_level_button, menu_button = draw_win_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if next_level_button.collidepoint(mouse_pos):
                    main(level + 1, unlocked_levels)
                    return
                if menu_button.collidepoint(mouse_pos):
                    main_menu(unlocked_levels)
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    main(level + 1, unlocked_levels)
                    return
                if event.key == pygame.K_m:
                    main_menu(unlocked_levels)
                    return
        if not pygame.display.get_init():
            won = False

def main(level=1, unlocked_levels=1):
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    player = YELLOW_SPACE_SHIP
    player_x, player_y = WIDTH // 2, HEIGHT - 100  # Spawn at the bottom center
    player_vel = 5
    bullet_vel = 7
    bullets = []
    enemies = []
    health_packs = []
    wave_length = 5
    enemy_vel = 1
    player_health = 100
    player_lives = 5
    max_enemies = 10
    total_enemies_spawned = 0
    total_kills = 0
    health_pack_timer = 0

    def redraw_window():
        draw_window(BG, player, player_x, player_y, bullets, player_health, health_packs)
        for enemy in enemies:
            enemy.draw(game_window)
        draw_lives(player_lives)
        draw_kills(total_kills)
        draw_level(level)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        health_pack_timer += 1
        if health_pack_timer >= 5 * FPS:
            health_pack = pygame.Rect(random.randrange(50, WIDTH-50), random.randrange(-1500, -100), 30, 30)
            health_packs.append(health_pack)
            health_pack_timer = 0

        if len(enemies) == 0 and total_enemies_spawned < max_enemies:
            for i in range(min(wave_length, max_enemies - total_enemies_spawned)):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green", "blue"]))
                enemies.append(enemy)
                total_enemies_spawned += 1

        if total_enemies_spawned == max_enemies and len(enemies) == 0:
            if level == unlocked_levels:
                unlocked_levels += 1
            win_menu(level, unlocked_levels)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player_x + player.get_width() // 2 - YELLOW_BULLET.get_width() // 2, player_y - 10, 4, 10)
                    bullets.append(bullet)
                    BULLET_SOUND.play()  # Play bullet sound
                if event.key == pygame.K_p:
                    pause_menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x - player_vel > 0:  # Move left
            player_x -= player_vel
        if keys[pygame.K_d] and player_x + player_vel + player.get_width() < WIDTH:  # Move right
            player_x += player_vel
        if keys[pygame.K_w] and player_y - player_vel > 0:  # Move up
            player_y -= player_vel
        if keys[pygame.K_s] and player_y + player_vel + player.get_height() < HEIGHT:  # Move down
            player_y += player_vel

        player_rect = pygame.Rect(player_x, player_y, player.get_width(), player.get_height())

        for bullet in bullets[:]:
            bullet.y -= bullet_vel
            if bullet.y < 0:
                bullets.remove(bullet)

        for health_pack in health_packs[:]:
            health_pack.y += 2
            if health_pack.colliderect(player_rect):
                player_health = min(player_health + 20, 100)
                health_packs.remove(health_pack)
            elif health_pack.y > HEIGHT:
                health_packs.remove(health_pack)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            player_health = enemy.move_bullets(bullet_vel, player_rect, player_health, level)
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            for bullet in bullets:
                if enemy.mask.overlap(pygame.mask.from_surface(YELLOW_BULLET), (bullet.x - enemy.x, bullet.y - enemy.y)):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    total_kills += 1
                    break
            for enemy_bullet in enemy.bullets[:]:
                for player_bullet in bullets[:]:
                    if enemy_bullet.colliderect(player_bullet):
                        enemy.bullets.remove(enemy_bullet)
                        bullets.remove(player_bullet)
                        break
            if enemy.y + enemy.ship_img.get_height() > HEIGHT:
                enemies.remove(enemy)
                player_lives -= 1
                if player_lives == 0:
                    run = False

        if player_health <= 0:
            run = False

    if player_health <= 0 or player_lives == 0:
        lost_menu(total_kills, unlocked_levels)
    pygame.quit()
    return level

if __name__ == "__main__":
    main_menu()