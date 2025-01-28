import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

GRASS = pygame.transform.scale(pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Car_Racing\Assets\Images\grass.jpg'), (WIDTH, HEIGHT))

TRACK = pygame.transform.scale(pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Car_Racing\Assets\Images\track.png'), (WIDTH, HEIGHT))

TRACK_BORDER = pygame.transform.scale(pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Car_Racing\Assets\Images\track-border.png'), (WIDTH, HEIGHT))

FINISH_LINE = pygame.transform.scale(pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Car_Racing\Assets\Images\finish.png'), (73,15))

RED_CAR = pygame.transform.scale(pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Car_Racing\Assets\Images\red-car.png'), (20, 30))
GREEN_CAR = pygame.transform.scale(pygame.image.load(r'C:\Users\Scp\Desktop\Python\My_Games\Car_Racing\Assets\Images\green-car.png'), (20, 30))

BG_MUSIC = pygame.mixer.music.load(r'C:\Users\Scp\Desktop\Python\My_Games\Car_Racing\Assets\Sounds\bg_music.mp3')

game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing")

def draw(GRASS, TRACK, FINISH_LINE, red_car_pos, green_car_pos, red_car_angle, green_car_angle, red_rounds, green_rounds):
    game_window.blit(GRASS, (0, 0))
    game_window.blit(TRACK, (0, 0))
    game_window.blit(TRACK_BORDER, (0, 0))  # Add the track border
    finish_line_x = WIDTH // 4.5 - FINISH_LINE.get_width() // 2
    finish_line_y = HEIGHT // 5 - FINISH_LINE.get_height() // 2
    game_window.blit(FINISH_LINE, (finish_line_x, finish_line_y))  # Center the finish line
    
    rotated_green_car = pygame.transform.rotate(GREEN_CAR, green_car_angle)
    rotated_red_car = pygame.transform.rotate(RED_CAR, red_car_angle)
    
    game_window.blit(rotated_green_car, green_car_pos)  # Position the green car
    game_window.blit(rotated_red_car, red_car_pos)  # Position the red car
    
    font = pygame.font.Font(None, 48)  # Increase font size for better visibility
    green_rounds_text = font.render(f'Green Rounds: {green_rounds}', True, (0, 255, 0))
    red_rounds_text = font.render(f'Red Rounds: {red_rounds}', True, (255, 0, 0))
    game_window.blit(green_rounds_text, (10, 10))  # Left-hand side
    game_window.blit(red_rounds_text, (WIDTH - red_rounds_text.get_width() - 10, 10))  # Right-hand side
    
    pygame.display.update()

def draw_buttons():
    font = pygame.font.Font(None, 60)  # Increase font size
    start_text = font.render('Start', True, (255, 255, 255))  # White color
    exit_text = font.render('Exit', True, (255, 255, 255))  # White color
    start_button = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    exit_button = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    game_window.blit(start_text, start_button)
    game_window.blit(exit_text, exit_button)
    pygame.display.update()
    return start_button, exit_button

def draw_pause_buttons():
    font = pygame.font.Font(None, 60)  # Increase font size
    unpause_text = font.render('Unpause', True, (255, 255, 255))  # White color
    restart_text = font.render('Restart', True, (255, 255, 255))  # White color
    exit_text = font.render('Exit', True, (255, 255, 255))  # White color
    unpause_button = unpause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    restart_button = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    exit_button = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    game_window.blit(unpause_text, unpause_button)
    game_window.blit(restart_text, restart_button)
    game_window.blit(exit_text, exit_button)
    pygame.display.update()
    return unpause_button, restart_button, exit_button

def countdown():
    font = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):
        game_window.blit(GRASS, (0, 0))  # Use the existing background
        game_window.blit(TRACK, (0, 0))  # Draw the track
        countdown_text = font.render(str(i), True, (255, 255, 255))
        game_window.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(1000)

def main_menu():
    run = True
    while run:
        game_window.blit(GRASS, (0, 0))  # Use the existing background
        game_window.blit(TRACK, (0, 0))  # Draw the track
        start_button, exit_button = draw_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    countdown()  # Add countdown before starting the game
                    run = False
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        pygame.display.update()

def pause_menu():
    paused = True
    while paused:
        game_window.blit(GRASS, (0, 0))  # Use the existing background
        game_window.blit(TRACK, (0, 0))  # Draw the track
        unpause_button, restart_button, exit_button = draw_pause_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if unpause_button.collidepoint(event.pos):
                    paused = False
                elif restart_button.collidepoint(event.pos):
                    return True  # Indicate that the game should be restarted
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        pygame.display.update()
    return False  # Indicate that the game should not be restarted

def draw_winner(winner):
    font = pygame.font.Font(None, 100)
    winner_text = font.render(f'{winner} Wins!', True, (255, 255, 255))
    game_window.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    while True:
        main_menu()
        pygame.mixer.music.play(-1)  # Play background music in an infinite loop
        run = True
        red_car_pos = [WIDTH // 4.5 - FINISH_LINE.get_width() // 2 + GREEN_CAR.get_width(), HEIGHT // 5 - FINISH_LINE.get_height() // 2 - RED_CAR.get_height()]
        green_car_pos = [WIDTH // 4.5 - FINISH_LINE.get_width() // 2, HEIGHT // 5 - FINISH_LINE.get_height() // 2 - GREEN_CAR.get_height()]
        red_car_angle = 0
        green_car_angle = 0
        red_rounds = 0
        green_rounds = 0
        red_crossed = False
        green_crossed = False

        track_mask = pygame.mask.from_surface(TRACK_BORDER)
        finish_line_mask = pygame.mask.from_surface(FINISH_LINE)
        finish_line_x = WIDTH // 4.5 - FINISH_LINE.get_width() // 2
        finish_line_y = HEIGHT // 5 - FINISH_LINE.get_height() // 2

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if pause_menu():
                        run = False  # Restart the game
                        break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                new_pos = [red_car_pos[0] - 5, red_car_pos[1]]
                if track_mask.overlap_area(pygame.mask.Mask((RED_CAR.get_width(), RED_CAR.get_height()), fill=True), (new_pos[0], new_pos[1])) == 0:
                    red_car_pos[0] -= 5
                    red_car_angle += 5
            if keys[pygame.K_RIGHT]:
                new_pos = [red_car_pos[0] + 5, red_car_pos[1]]
                if track_mask.overlap_area(pygame.mask.Mask((RED_CAR.get_width(), RED_CAR.get_height()), fill=True), (new_pos[0], new_pos[1])) == 0:
                    red_car_pos[0] += 5
                    red_car_angle -= 5
            if keys[pygame.K_UP]:
                new_pos = [red_car_pos[0], red_car_pos[1] - 5]
                if track_mask.overlap_area(pygame.mask.Mask((RED_CAR.get_width(), RED_CAR.get_height()), fill=True), (new_pos[0], new_pos[1])) == 0:
                    red_car_pos[1] -= 5
                    red_car_angle = 0
            if keys[pygame.K_DOWN]:
                new_pos = [red_car_pos[0], red_car_pos[1] + 5]
                if track_mask.overlap_area(pygame.mask.Mask((RED_CAR.get_width(), RED_CAR.get_height()), fill=True), (new_pos[0], new_pos[1])) == 0 and red_car_pos[1] + RED_CAR.get_height() < HEIGHT and not finish_line_mask.overlap_area(pygame.mask.Mask((RED_CAR.get_width(), RED_CAR.get_height()), fill=True), (new_pos[0] - finish_line_x, new_pos[1] - finish_line_y)) > 0:
                    red_car_pos[1] += 5
                    red_car_angle = 180
            if keys[pygame.K_a]:
                new_pos = [green_car_pos[0] - 5, green_car_pos[1]]
                if track_mask.overlap_area(pygame.mask.Mask((GREEN_CAR.get_width(), GREEN_CAR.get_height()), fill=True), (new_pos[0], new_pos[1])) == 0:
                    green_car_pos[0] -= 5
                    green_car_angle += 5
            if keys[pygame.K_d]:
                new_pos = [green_car_pos[0] + 5, green_car_pos[1]]
                if track_mask.overlap_area(pygame.mask.Mask((GREEN_CAR.get_width(), GREEN_CAR.get_height()), fill=True), (new_pos[0], new_pos[1])) == 0:
                    green_car_pos[0] += 5
                    green_car_angle -= 5
            if keys[pygame.K_w]:
                new_pos = [green_car_pos[0], green_car_pos[1] - 5]
                if track_mask.overlap_area(pygame.mask.Mask((GREEN_CAR.get_width(), GREEN_CAR.get_height()), fill=True), (new_pos[0], new_pos[1])) == 0:
                    green_car_pos[1] -= 5
                    green_car_angle = 0
            if keys[pygame.K_s]:
                new_pos = [green_car_pos[0], green_car_pos[1] + 5]
                if track_mask.overlap_area(pygame.mask.Mask((GREEN_CAR.get_width(), GREEN_CAR.get_height()), fill=True), (new_pos[0], new_pos[1])) == 0 and green_car_pos[1] + GREEN_CAR.get_height() < HEIGHT and not finish_line_mask.overlap_area(pygame.mask.Mask((GREEN_CAR.get_width(), GREEN_CAR.get_height()), fill=True), (new_pos[0] - finish_line_x, new_pos[1] - finish_line_y)) > 0:
                    green_car_pos[1] += 5
                    green_car_angle = 180

            # Check if cars cross the finish line
            if finish_line_mask.overlap_area(pygame.mask.Mask((RED_CAR.get_width(), RED_CAR.get_height()), fill=True), (red_car_pos[0] - finish_line_x, red_car_pos[1] - finish_line_y)) > 0:
                if not red_crossed and red_car_pos[1] < finish_line_y:
                    red_rounds += 1
                    red_crossed = True
            else:
                red_crossed = False

            if finish_line_mask.overlap_area(pygame.mask.Mask((GREEN_CAR.get_width(), GREEN_CAR.get_height()), fill=True), (green_car_pos[0] - finish_line_x, green_car_pos[1] - finish_line_y)) > 0:
                if not green_crossed and green_car_pos[1] < finish_line_y:
                    green_rounds += 1
                    green_crossed = True
            else:
                green_crossed = False

            # Check for winner
            if red_rounds >= 3:
                draw_winner("Red")
                run = False
            elif green_rounds >= 3:
                draw_winner("Green")
                run = False

            draw(GRASS, TRACK, FINISH_LINE, red_car_pos, green_car_pos, red_car_angle, green_car_angle, red_rounds, green_rounds)
        pygame.mixer.music.stop()

if __name__ == "__main__":
    main()