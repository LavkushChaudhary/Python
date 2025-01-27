import pygame
import time
import random

# Set up display
WIDTH = 1200
HEIGHT = 600
game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighter")

# Define game constants
BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)
FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 10
GRENADE_VELOCITY = 7
MAX_BULLETS = 5
TOTAL_BULLETS = 20
TOTAL_GRENADES = 3
SPACESHIPS_WIDTH = 70
SPACESHIPS_HEIGHT = 55

# Load spaceship images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Galaxy_Fighters\spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Galaxy_Fighters\spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT)), 270)

# Load sound effects
BULLET_SOUND = r'C:\Users\Scp\Desktop\Python\My_Games\Galaxy_Fighters\Gun+Silencer.mp3'
GRENADE_SOUND = r'C:\Users\Scp\Desktop\Python\My_Games\Galaxy_Fighters\Grenade+1.mp3'
BACKGROUND_MUSIC = r'C:\Users\Scp\Desktop\Python\My_Games\Galaxy_Fighters\backgroundmusic.mp3'

# Initial health values
YELLOW_HEALTH = 100
RED_HEALTH = 100

# Score tracking
yellow_score = 0
red_score = 0

# Power-ups
POWER_UPS = ['speed', 'invincibility', 'extra_bullets']
power_up_active = False
power_up_type = None
power_up_timer = 0

# Health packs
HEALTH_PACKS = []
HEALTH_PACK_VALUE = 20

# Bullet packs
BULLET_PACKS = []
BULLET_PACK_VALUE = 5

# Grenade packs
GRENADE_PACKS = []
GRENADE_PACK_VALUE = 2

# Difficulty levels
DIFFICULTY_LEVELS = {
    'easy': {'velocity': 3, 'bullet_velocity': 6, 'grenade_velocity': 4},
    'medium': {'velocity': 5, 'bullet_velocity': 10, 'grenade_velocity': 7},
    'hard': {'velocity': 7, 'bullet_velocity': 14, 'grenade_velocity': 11},
    'extreme': {'velocity': 10, 'bullet_velocity': 20, 'grenade_velocity': 15}  # New difficulty level
}
current_difficulty = 'medium'

# Handle yellow spaceship movement
def handle_yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width <= BORDER.x:
        yellow.x += VELOCITY
    if key_pressed[pygame.K_a] and yellow.x - VELOCITY >= 0:
        yellow.x -= VELOCITY
    if key_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height <= HEIGHT - 15:
        yellow.y += VELOCITY
    if key_pressed[pygame.K_w] and yellow.y - VELOCITY >= 0:
        yellow.y -= VELOCITY

# Handle red spaceship movement
def handle_red_movement(key_pressed, red):
    if key_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width <= WIDTH:
        red.x += VELOCITY
    if key_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    if key_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height <= HEIGHT - 15:
        red.y += VELOCITY
    if key_pressed[pygame.K_UP] and red.y - VELOCITY >= 0:
        red.y -= VELOCITY

# Handle bullet movement and collisions
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    global YELLOW_HEALTH, RED_HEALTH
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if bullet.colliderect(red):
            RED_HEALTH -= 10  # Bullet hit reduces health
            yellow_bullets.remove(bullet)
            if RED_HEALTH <= 0:
                RED_HEALTH = 0
                return True  # Indicate that the player has died
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if bullet.colliderect(yellow):
            YELLOW_HEALTH -= 10  # Bullet hit reduces health
            red_bullets.remove(bullet)
            if YELLOW_HEALTH <= 0:
                YELLOW_HEALTH = 0
                return True  # Indicate that the player has died
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    return False

# Handle grenade movement and collisions
def handle_grenades(yellow_grenades, red_grenades, yellow, red):
    global YELLOW_HEALTH, RED_HEALTH
    for grenade in yellow_grenades:
        grenade.x += GRENADE_VELOCITY
        if grenade.colliderect(red):
            RED_HEALTH -= 20  # Grenade hit reduces more health
            yellow_grenades.remove(grenade)
            if RED_HEALTH <= 0:
                RED_HEALTH = 0
                return True  # Indicate that the player has died
        elif grenade.x > WIDTH:
            yellow_grenades.remove(grenade)
    for grenade in red_grenades:
        grenade.x -= GRENADE_VELOCITY
        if grenade.colliderect(yellow):
            YELLOW_HEALTH -= 20  # Grenade hit reduces more health
            red_grenades.remove(grenade)
            if YELLOW_HEALTH <= 0:
                YELLOW_HEALTH = 0
                return True  # Indicate that the player has died
        elif grenade.x < 0:
            red_grenades.remove(grenade)
    return False

# Handle power-ups
def handle_power_ups(yellow, red):
    global power_up_active, power_up_type, power_up_timer
    if power_up_active:
        if time.time() - power_up_timer > 10:  # Power-up lasts for 10 seconds
            power_up_active = False
            power_up_type = None
    else:
        if random.randint(1, 1000) == 1:  # Random chance to spawn a power-up
            power_up_type = random.choice(POWER_UPS)
            power_up_active = True
            power_up_timer = time.time()

    if power_up_active:
        if power_up_type == 'speed':
            VELOCITY = DIFFICULTY_LEVELS[current_difficulty]['velocity'] * 2
        elif power_up_type == 'invincibility':
            # Implement invincibility logic
            pass
        elif power_up_type == 'extra_bullets':
            # Implement extra bullets logic
            pass

# Handle health packs
def handle_health_packs(yellow, red):
    global YELLOW_HEALTH, RED_HEALTH
    for pack in HEALTH_PACKS:
        if yellow.colliderect(pack):
            YELLOW_HEALTH = min(100, YELLOW_HEALTH + HEALTH_PACK_VALUE)
            HEALTH_PACKS.remove(pack)
        elif red.colliderect(pack):
            RED_HEALTH = min(100, RED_HEALTH + HEALTH_PACK_VALUE)
            HEALTH_PACKS.remove(pack)

# Function to spawn bullet packs
def spawn_bullet_packs():
    pack_x = random.randint(0, WIDTH - 20)
    pack_y = random.randint(0, HEIGHT - 20)
    BULLET_PACKS.append(pygame.Rect(pack_x, pack_y, 20, 20))

# Function to spawn grenade packs
def spawn_grenade_packs():
    pack_x = random.randint(0, WIDTH - 20)
    pack_y = random.randint(0, HEIGHT - 20)
    GRENADE_PACKS.append(pygame.Rect(pack_x, pack_y, 20, 20))

# Handle bullet packs
def handle_bullet_packs(yellow, red):
    global yellow_bullet_count, red_bullet_count
    for pack in BULLET_PACKS:
        if yellow.colliderect(pack):
            yellow_bullet_count = min(TOTAL_BULLETS, yellow_bullet_count + BULLET_PACK_VALUE)
            BULLET_PACKS.remove(pack)
        elif red.colliderect(pack):
            red_bullet_count = min(TOTAL_BULLETS, red_bullet_count + BULLET_PACK_VALUE)
            BULLET_PACKS.remove(pack)

# Handle grenade packs
def handle_grenade_packs(yellow, red):
    global yellow_grenade_count, red_grenade_count  # Declare global variables
    for pack in GRENADE_PACKS:
        if yellow.colliderect(pack):
            yellow_grenade_count = min(TOTAL_GRENADES, yellow_grenade_count + GRENADE_PACK_VALUE)
            GRENADE_PACKS.remove(pack)
        elif red.colliderect(pack):
            red_grenade_count = min(TOTAL_GRENADES, red_grenade_count + GRENADE_PACK_VALUE)
            GRENADE_PACKS.remove(pack)

# Function to set difficulty
def set_difficulty(level):
    global VELOCITY, BULLET_VELOCITY, GRENADE_VELOCITY
    VELOCITY = DIFFICULTY_LEVELS[level]['velocity']
    BULLET_VELOCITY = DIFFICULTY_LEVELS[level]['bullet_velocity']
    GRENADE_VELOCITY = DIFFICULTY_LEVELS[level]['grenade_velocity']

# Function to spawn health packs
def spawn_health_packs():
    pack_x = random.randint(0, WIDTH - 20)
    pack_y = random.randint(0, HEIGHT - 20)
    HEALTH_PACKS.append(pygame.Rect(pack_x, pack_y, 20, 20))

# Draw game window
def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_bullet_count, red_bullet_count, yellow_grenades, red_grenades, yellow_grenade_count, red_grenade_count, background):
    game_window.blit(background, (0, 0))  # Draw the background first
    pygame.draw.rect(game_window, 'black', BORDER)
    game_window.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    game_window.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(game_window, 'yellow', bullet)
    for bullet in red_bullets:
        pygame.draw.rect(game_window, 'red', bullet)
    for grenade in yellow_grenades:
        pygame.draw.circle(game_window, 'yellow', (grenade.x + grenade.width // 2, grenade.y + grenade.height // 2), 10)
    for grenade in red_grenades:
        pygame.draw.circle(game_window, 'red', (grenade.x + grenade.width // 2, grenade.y + grenade.height // 2), 10)
    for pack in HEALTH_PACKS:
        pygame.draw.rect(game_window, 'green', pack)
    for pack in BULLET_PACKS:
        pygame.draw.rect(game_window, 'blue', pack)
    for pack in GRENADE_PACKS:
        pygame.draw.rect(game_window, 'purple', pack)
    yellow_bullet_text = pygame.font.SysFont('comicsans', 20).render(f'Yellow Bullets: {yellow_bullet_count}', 1, 'white')
    red_bullet_text = pygame.font.SysFont('comicsans', 20).render(f'Red Bullets: {red_bullet_count}', 1, 'white')
    yellow_grenade_text = pygame.font.SysFont('comicsans', 20).render(f'Yellow Grenades: {yellow_grenade_count}', 1, 'white')
    red_grenade_text = pygame.font.SysFont('comicsans', 20).render(f'Red Grenades: {red_grenade_count}', 1, 'white')
    yellow_health_text = pygame.font.SysFont('comicsans', 20).render(f'Yellow Health: {YELLOW_HEALTH}', 1, 'white')
    red_health_text = pygame.font.SysFont('comicsans', 20).render(f'Red Health: {RED_HEALTH}', 1, 'white')
    yellow_score_text = pygame.font.SysFont('comicsans', 20).render(f'Yellow Score: {yellow_score}', 1, 'white')
    red_score_text = pygame.font.SysFont('comicsans', 20).render(f'Red Score: {red_score}', 1, 'white')
    game_window.blit(yellow_bullet_text, (10, 10))
    game_window.blit(red_bullet_text, (WIDTH - red_bullet_text.get_width() - 10, 10))
    game_window.blit(yellow_grenade_text, (10, 40))
    game_window.blit(red_grenade_text, (WIDTH - red_grenade_text.get_width() - 10, 40))
    game_window.blit(yellow_health_text, (10, 70))
    game_window.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 70))
    game_window.blit(yellow_score_text, (10, 100))
    game_window.blit(red_score_text, (WIDTH - red_score_text.get_width() - 10, 100))
    pygame.display.update()

# Draw start screen
def draw_start_screen(background):
    game_window.blit(background, (0, 0))  # Draw the background first
    font = pygame.font.SysFont('comicsans', 50)
    start_text = font.render('Start Game', 1, 'white')
    start_button = pygame.Rect(WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2, start_text.get_width(), start_text.get_height())
    game_window.blit(start_text, (start_button.x, start_button.y))
    pygame.display.update()
    return start_button

# Draw difficulty selection screen
def draw_difficulty_screen(background):
    game_window.blit(background, (0, 0))  # Draw the background first
    font = pygame.font.SysFont('comicsans', 50)
    easy_text = font.render('Easy', 1, 'white')
    medium_text = font.render('Medium', 1, 'white')
    hard_text = font.render('Hard', 1, 'white')
    extreme_text = font.render('Extreme', 1, 'white')
    easy_button = pygame.Rect(WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 100, easy_text.get_width(), easy_text.get_height())
    medium_button = pygame.Rect(WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 - 50, medium_text.get_width(), medium_text.get_height())
    hard_button = pygame.Rect(WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2, hard_text.get_width(), hard_text.get_height())
    extreme_button = pygame.Rect(WIDTH // 2 - extreme_text.get_width() // 2, HEIGHT // 2 + 50, extreme_text.get_width(), extreme_text.get_height())
    game_window.blit(easy_text, (easy_button.x, easy_button.y))
    game_window.blit(medium_text, (medium_button.x, medium_button.y))
    game_window.blit(hard_text, (hard_button.x, hard_button.y))
    game_window.blit(extreme_text, (extreme_button.x, extreme_button.y))
    pygame.display.update()
    return easy_button, medium_button, hard_button, extreme_button

# Draw restart and exit buttons
def draw_buttons():
    font = pygame.font.SysFont('comicsans', 30)
    restart_text = font.render('Restart', 1, 'white')
    exit_text = font.render('Exit', 1, 'white')
    restart_button = pygame.Rect(WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50, restart_text.get_width(), restart_text.get_height())
    exit_button = pygame.Rect(WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 100, exit_text.get_width(), exit_text.get_height())
    game_window.blit(restart_text, (restart_button.x, restart_button.y))
    game_window.blit(exit_text, (exit_button.x, exit_button.y))
    pygame.display.update()
    return restart_button, exit_button

# Reset game state
def reset_game():
    global YELLOW_HEALTH, RED_HEALTH, yellow_score, red_score, HEALTH_PACKS
    YELLOW_HEALTH = 100
    RED_HEALTH = 100
    yellow_score = 0
    red_score = 0
    HEALTH_PACKS = []

# Show winner and display buttons
def show_winner(winner):
    time.sleep(1)  # Add a delay of 1 second before showing the winning message
    font = pygame.font.SysFont('comicsans', 50)
    winner_text = font.render(f'{winner} Win!', 1, 'white')  # Change color to white
    game_window.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    time.sleep(2)  # Add a delay of 2 seconds before showing the buttons
    restart_button, exit_button = draw_buttons()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    reset_game()
                    return True
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return False

# Draw pause screen with options
def draw_pause_screen():
    font = pygame.font.SysFont('comicsans', 50)
    pause_text = font.render('Paused', 1, 'white')
    unpause_text = font.render('Unpause', 1, 'white')
    exit_text = font.render('Exit', 1, 'white')
    unpause_button = pygame.Rect(WIDTH // 2 - unpause_text.get_width() // 2, HEIGHT // 2 - 50, unpause_text.get_width(), unpause_text.get_height())
    exit_button = pygame.Rect(WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50, exit_text.get_width(), exit_text.get_height())
    game_window.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 150))
    game_window.blit(unpause_text, (unpause_button.x, unpause_button.y))
    game_window.blit(exit_text, (exit_button.x, exit_button.y))
    pygame.display.update()
    return unpause_button, exit_button

# Function to select difficulty
def select_difficulty(background):
    easy_button, medium_button, hard_button, extreme_button = draw_difficulty_screen(background)
    selecting_difficulty = True
    while selecting_difficulty:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_pos):
                    return 'easy'
                elif medium_button.collidepoint(mouse_pos):
                    return 'medium'
                elif hard_button.collidepoint(mouse_pos):
                    return 'hard'
                elif extreme_button.collidepoint(mouse_pos):
                    return 'extreme'

# Main game loop
def main():
    global red_score, yellow_score, VELOCITY, BULLET_VELOCITY, GRENADE_VELOCITY, yellow_grenade_count, red_grenade_count, yellow_bullet_count, red_bullet_count  # Declare global variables
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # Load and scale the background only once
    background = pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Galaxy_Fighters\space.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale the background to fit the screen

    # Play background music
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1)

    start_button = draw_start_screen(background)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    waiting = False

    current_difficulty = select_difficulty(background)
    if current_difficulty is None:
        return

    set_difficulty(current_difficulty)  # Set initial difficulty

    while True:
        red = pygame.Rect(1150, 250, SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT)
        yellow = pygame.Rect(0, 250, SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT)

        yellow_bullets = []
        red_bullets = []
        yellow_grenades = []
        red_grenades = []
        yellow_bullet_count = TOTAL_BULLETS
        red_bullet_count = TOTAL_BULLETS
        yellow_grenade_count = TOTAL_GRENADES
        red_grenade_count = TOTAL_GRENADES

        yellow_last_bullet_time = time.time()
        red_last_bullet_time = time.time()
        last_pack_spawn_time = time.time()

        clock = pygame.time.Clock()

        yellow_grenade_held = False
        red_grenade_held = False

        run = True
        paused = False
        while run:
            clock.tick(FPS)
            current_time = time.time()

            # Add bullets back after 10 seconds
            if current_time - yellow_last_bullet_time >= 10 and yellow_bullet_count < TOTAL_BULLETS:
                yellow_bullet_count += 1
                yellow_last_bullet_time = current_time

            if current_time - red_last_bullet_time >= 10 and red_bullet_count < TOTAL_BULLETS:
                red_bullet_count += 1
                red_last_bullet_time = current_time

            # Spawn packs every 10 seconds
            if current_time - last_pack_spawn_time >= 10:
                spawn_health_packs()
                spawn_bullet_packs()
                spawn_grenade_packs()
                last_pack_spawn_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            unpause_button, exit_button = draw_pause_screen()
                        else:
                            pygame.display.update()

                if paused:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if unpause_button.collidepoint(mouse_pos):
                            paused = False
                            pygame.display.update()
                        elif exit_button.collidepoint(mouse_pos):
                            pygame.quit()
                            return

                if not paused:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS and yellow_bullet_count > 0:
                            bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                            yellow_bullets.append(bullet)
                            yellow_bullet_count -= 1
                            pygame.mixer.Sound(BULLET_SOUND).play()

                        if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS and red_bullet_count > 0:
                            bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                            red_bullets.append(bullet)
                            red_bullet_count -= 1
                            pygame.mixer.Sound(BULLET_SOUND).play()

                        if event.key == pygame.K_LCTRL and yellow_grenade_count > 0:
                            yellow_grenade_held = True

                        if event.key == pygame.K_RCTRL and red_grenade_count > 0:
                            red_grenade_held = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LCTRL and yellow_grenade_held:
                            grenade = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 10, 20, 20)
                            yellow_grenades.append(grenade)
                            yellow_grenade_count -= 1
                            pygame.mixer.Sound(GRENADE_SOUND).play()
                            yellow_grenade_held = False

                        if event.key == pygame.K_RCTRL and red_grenade_held:
                            grenade = pygame.Rect(red.x - 20, red.y + red.height // 2 - 10, 20, 20)
                            red_grenades.append(grenade)
                            red_grenade_count -= 1
                            pygame.mixer.Sound(GRENADE_SOUND).play()
                            red_grenade_held = False

            if not paused:
                key_pressed = pygame.key.get_pressed()
                handle_red_movement(key_pressed, red)
                handle_yellow_movement(key_pressed, yellow)

                if handle_bullets(yellow_bullets, red_bullets, yellow, red) or handle_grenades(yellow_grenades, red_grenades, yellow, red):
                    if YELLOW_HEALTH <= 0:
                        red_score += 1
                        if not show_winner("Right Side Player"):  # Use "Right Side Player" here
                            return
                        current_difficulty = select_difficulty(background)
                        if current_difficulty is None:
                            return
                        set_difficulty(current_difficulty)
                        break
                    elif RED_HEALTH <= 0:
                        yellow_score += 1
                        if not show_winner("Left Side Player"):  # Use "Left Side Player" here
                            return
                        current_difficulty = select_difficulty(background)
                        if current_difficulty is None:
                            return
                        set_difficulty(current_difficulty)
                        break

                handle_power_ups(yellow, red)
                handle_health_packs(yellow, red)
                handle_bullet_packs(yellow, red)
                handle_grenade_packs(yellow, red)

                draw_window(red, yellow, yellow_bullets, red_bullets, yellow_bullet_count, red_bullet_count, yellow_grenades, red_grenades, yellow_grenade_count, red_grenade_count, background)

    pygame.quit()

if __name__ == '__main__':
    main()