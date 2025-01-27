import pygame
import time
import random
import os  # For handling file paths

# Initialize all imported pygame modules
pygame.init()
pygame.font.init()

# Initializing height and width for the game
WIDTH, HEIGHT = 1000, 600
PLAYER_HEIGHT, PLAYER_WIDTH = 40, 40
STAR_WIDTH, STAR_HEIGHT = 20, 40

# Player velocity is used to move the player
PLAYER_VELOCITY = 6
STAR_VELOCITY = 5

# Setting font for showing the survival time
FONT = pygame.font.SysFont("ALGERIAN", 30)

# Creating game window and setting caption of the game
game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Adding background image (use relative path)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
BG_IMAGE_PATH = os.path.join(ASSETS_DIR, r'C:\Users\Scp\Desktop\Python\My_Games\Space_Dodge\space.jpg')
BG = pygame.transform.scale(pygame.image.load(BG_IMAGE_PATH), (WIDTH, HEIGHT))

# Set the new path for the high score file
HIGH_SCORE_FILE = r'C:\Users\Scp\Desktop\Python\My_Games\Space_Dodge\high_score.txt'

def load_high_score():
    """Load the high score from a file."""
    if os.path.exists(HIGH_SCORE_FILE):  # Check if the file exists
        with open(HIGH_SCORE_FILE, 'r') as file:
            return float(file.read().strip())  # Return the score as a float
    return 0  # Default high score if no file exists

def save_high_score(score):
    """Save the high score to a file."""
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))  # Write the high score to the file

def draw_start_screen(high_score):
    """Display the start screen with Start and Exit buttons and high score."""
    game_window.blit(BG, (0, 0))  # Draw the background
    title_text = FONT.render("Space Dodge", 1, 'white')  # Title text
    high_score_text = FONT.render(f"High Score: {round(high_score, 1)}s", 1, 'white')  # High score text
    start_button_text = FONT.render("Start", 1, 'black')  # Start button text
    exit_button_text = FONT.render("Exit", 1, 'black')  # Exit button text

    # Draw title
    game_window.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 3))
    game_window.blit(high_score_text, (WIDTH / 2 - high_score_text.get_width() / 2, HEIGHT / 2 - 50))

    # Draw start button
    start_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50)  # Define start button position and size
    pygame.draw.rect(game_window, 'white', start_button)  # Draw start button background
    game_window.blit(start_button_text, (WIDTH / 2 - start_button_text.get_width() / 2, HEIGHT / 2 + 10))  # Draw text

    # Draw exit button
    exit_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 80, 200, 50)  # Define exit button position and size
    pygame.draw.rect(game_window, 'white', exit_button)  # Draw exit button background
    game_window.blit(exit_button_text, (WIDTH / 2 - exit_button_text.get_width() / 2, HEIGHT / 2 + 90))  # Draw text

    pygame.display.update()  # Update the display to show everything
    return start_button, exit_button  # Return both buttons

def draw_game_screen(player, elapsed_time, stars, high_score):
    """Draw game elements on the screen."""
    game_window.blit(BG, (0, 0))  # Draw the background
    survival_time = FONT.render(f'Survival Time: {round(elapsed_time, 1)}s', 1, 'white')  # Survival time text
    high_score_text = FONT.render(f'High Score: {round(high_score, 1)}s', 1, 'white')  # High score text

    # Display survival time and high score
    game_window.blit(survival_time, (10, 10))
    game_window.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

    # Draw player and stars
    pygame.draw.rect(game_window, 'yellow', player)
    for star in stars:
        pygame.draw.rect(game_window, 'white', star)
    pygame.display.update()  # Update the display

def game_over_screen(elapsed_time, high_score):
    """Display game-over screen with Start and Exit buttons, high score, and player's score."""
    # Display the death message with the player's score
    lost_text = FONT.render(f"You Died! Score: {round(elapsed_time, 1)}s. Click Start to Play Again", 1, 'white')
    high_score_text = FONT.render(f"High Score: {round(high_score, 1)}s", 1, 'white')  # High score text
    start_button_text = FONT.render("Start", 1, 'black')  # Start button text
    exit_button_text = FONT.render("Exit", 1, 'black')  # Exit button text

    # Draw the background
    game_window.blit(BG, (0, 0))
    
    # Display the "You Died!" message with the score
    game_window.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 3))  
    
    # Display the high score
    game_window.blit(high_score_text, (WIDTH / 2 - high_score_text.get_width() / 2, HEIGHT / 3 + 50))

    # Draw the start and exit buttons
    start_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50)
    pygame.draw.rect(game_window, 'white', start_button)  # Draw button background
    game_window.blit(start_button_text, (WIDTH / 2 - start_button_text.get_width() / 2, HEIGHT / 2 + 10))  # Draw text

    exit_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 80, 200, 50)
    pygame.draw.rect(game_window, 'white', exit_button)  # Draw button background
    game_window.blit(exit_button_text, (WIDTH / 2 - exit_button_text.get_width() / 2, HEIGHT / 2 + 90))  # Draw text

    pygame.display.update()  # Update the display
    return start_button, exit_button  # Return both buttons


def main_game_loop(high_score):
    """The main game loop, which resets when the player dies."""
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)  # Initialize player position
    clock = pygame.time.Clock()  # Game clock to control FPS
    start_time = time.time()  # Record start time
    elapsed_time = 0  # Time the player survives
    star_add_increment = 2000  # Time interval to spawn stars
    star_count = 0  # Star spawn counter
    stars = []  # List of stars in the game
    hit = False  # Flag to check if player collided with a star

    while not hit:
        star_count += clock.tick(60)  # Increment the star count
        elapsed_time = time.time() - start_time  # Calculate elapsed time

        # Add new stars at regular intervals
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(500, star_add_increment - 50)  # Decrease spawn interval for challenge
            star_count = 0  # Reset star count

        # Handle events (e.g., quitting the game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return high_score, False  # Exit the game

        # Player movement logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        # Move stars and check for collisions with the player
        for star in stars[:]:
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:  # Remove stars that go off the screen
                stars.remove(star)
            elif star.colliderect(player):  # If the player hits a star, end the game
                hit = True
                break

        draw_game_screen(player, elapsed_time, stars, high_score)  # Draw the game screen

    # Update the high score if necessary
    if elapsed_time > high_score:
        high_score = elapsed_time
        save_high_score(high_score)  # Save new high score

    return elapsed_time, high_score  # Return both the elapsed time and high score

def main():
    """Main loop to handle start, game, and restart screens."""
    high_score = load_high_score()  # Load the high score from file
    running = True

    while running:
        # Show the start screen
        start_button, exit_button = draw_start_screen(high_score)

        # Wait for the player to click Start or Exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Close the game window
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):  # Start button clicked
                        waiting = False
                    if exit_button.collidepoint(mouse_pos):  # Exit button clicked
                        pygame.quit()
                        return

        # Start the game loop
        elapsed_time, high_score = main_game_loop(high_score)

        # Show the game-over screen only after the player dies
        start_button, exit_button = game_over_screen(elapsed_time, high_score)

        # Wait for the player to click Start or Exit again
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):  # Start button clicked
                        waiting = False
                    if exit_button.collidepoint(mouse_pos):  # Exit button clicked
                        pygame.quit()
                        return

# Start the game when the script is executed
if __name__ == "__main__":
    main()