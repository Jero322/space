import pygame
import random
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # Power-up color

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Jumper")

# Clock to control game speed
clock = pygame.time.Clock()

# Font for text
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 24)

# High score file
HIGH_SCORE_FILE = "high_score.json"

# Power-up types and effects
POWER_UP_TYPES = {
    "slow_platforms": {"color": YELLOW, "duration": 10000, "effect": "slow platforms"},
    "high_jump": {"color": BLUE, "duration": 10000, "effect": "high jump"},
    "invincibility": {"color": RED, "duration": 10000, "effect": "invincibility"},
}

# Load high score
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return json.load(file)
    return 0  # Default high score if file doesn't exist

# Save high score
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump(score, file)

# Difficulty settings
def generate_platforms(num_platforms):
    platform_width = 100
    platform_height = 20
    platforms = []
    for i in range(num_platforms):
        platforms.append(pygame.Rect(random.randint(0, SCREEN_WIDTH - platform_width),
                                     random.randint(0, SCREEN_HEIGHT),
                                     platform_width, platform_height))
    return platforms

# Power-up generation
def generate_power_up():
    power_up_width = 30
    power_up_height = 30
    power_up_type = random.choice(list(POWER_UP_TYPES.keys()))
    power_up = {
        "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - power_up_width),
                            random.randint(0, SCREEN_HEIGHT - power_up_height),
                            power_up_width, power_up_height),
        "type": power_up_type,
        "color": POWER_UP_TYPES[power_up_type]["color"],
    }
    return power_up

# Home screen function
def home_screen(high_score):
    running = True
    while running:
        screen.fill(BLACK)
        title_text = font.render("Space Jumper", True, WHITE)
        start_text = small_font.render("Press ENTER to Start", True, WHITE)
        difficulty_text = small_font.render("Press D for Difficulty", True, WHITE)
        exit_text = small_font.render("Press ESC to Exit", True, WHITE)
        high_score_text = small_font.render(f"High Score: {high_score}", True, WHITE)

        # Center the text on the screen
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(difficulty_text, (SCREEN_WIDTH // 2 - difficulty_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    return "start"
                if event.key == pygame.K_d:  # Go to difficulty menu
                    return "difficulty"
                if event.key == pygame.K_ESCAPE:  # Exit the game
                    running = False

        pygame.display.flip()
        clock.tick(60)

# Difficulty menu function
def difficulty_screen():
    running = True
    while running:
        screen.fill(BLACK)
        
        # Title text at the top
        title_text = font.render("Select Difficulty", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Easy button
        easy_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50)
        pygame.draw.rect(screen, GREEN, easy_button)
        easy_text = small_font.render("Easy", True, BLACK)
        screen.blit(easy_text, (easy_button.x + easy_button.width // 2 - easy_text.get_width() // 2,
                                easy_button.y + easy_button.height // 2 - easy_text.get_height() // 2))

        # Medium button
        medium_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, BLUE, medium_button)
        medium_text = small_font.render("Medium", True, WHITE)
        screen.blit(medium_text, (medium_button.x + medium_button.width // 2 - medium_text.get_width() // 2,
                                  medium_button.y + medium_button.height // 2 - medium_text.get_height() // 2))

        # Hard button
        hard_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
        pygame.draw.rect(screen, RED, hard_button)
        hard_text = small_font.render("Hard", True, WHITE)
        screen.blit(hard_text, (hard_button.x + hard_button.width // 2 - hard_text.get_width() // 2,
                                hard_button.y + hard_button.height // 2 - hard_text.get_height() // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    return "easy"
                if medium_button.collidepoint(event.pos):
                    return "medium"
                if hard_button.collidepoint(event.pos):
                    return "hard"

        pygame.display.flip()
        clock.tick(60)

# Game Over screen function
def game_over_screen(score, high_score):
    running = True
    while running:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        high_score_text = small_font.render(f"High Score: {high_score}", True, WHITE)
        restart_text = small_font.render("Press ENTER to Restart", True, WHITE)
        exit_text = small_font.render("Press ESC to Exit", True, WHITE)

        # Center the text on the screen
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart the game
                    return True
                if event.key == pygame.K_ESCAPE:  # Exit the game
                    running = False

        pygame.display.flip()
        clock.tick(60)

# Main game function
# Main game function
def game_loop(platforms, difficulty):
    # Player settings
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - 50
    player_speed = 9

    # Game variables
    gravity = 0.25
    player_velocity = 0
    jump_strength = -10
    score = 0
    game_started = False

    # Difficulty-based settings
    platform_speed = 3  # Default medium speed
    if difficulty == "easy":
        platform_speed = 2
    elif difficulty == "hard":
        platform_speed = 5

    # Load high score
    high_score = load_high_score()

    # Power-up variables
    power_up = generate_power_up()
    active_power_up = None
    power_up_timer = 0

    # Power-up effects
    original_platform_speed = platform_speed
    original_jump_strength = jump_strength
    invincible = False

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                game_started = True
                player_velocity = jump_strength

        if game_started:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 50:
                player_x += player_speed

            # Apply gravity (unless invincible)
            if not invincible:
                player_velocity += gravity
            else:
                player_velocity = -2  # Float upward when invincible

            player_y += player_velocity

            if player_y < 0:
                player_y = 0
                player_velocity = 0

            # Jump if standing on a platform
            for platform in platforms:
                if player_velocity > 0 and platform.colliderect((player_x, player_y, 50, 50)):
                    if invincible:
                        platforms.remove(platform)  # Destroy platform if invincible
                    else:
                        player_velocity = jump_strength
                        score += 1

            # Collect power-up
            if pygame.Rect(player_x, player_y, 50, 50).colliderect(power_up["rect"]):
                active_power_up = power_up
                power_up_timer = pygame.time.get_ticks()
                power_up = generate_power_up()  # Generate a new power-up

                # Activate power-up effects
                if active_power_up["type"] == "slow_platforms":
                    platform_speed = 1  # Slow down platforms
                elif active_power_up["type"] == "high_jump":
                    jump_strength = -15  # Increase jump strength
                elif active_power_up["type"] == "invincibility":
                    invincible = True  # Enable invincibility

            # Apply power-up effects
            if active_power_up:
                current_time = pygame.time.get_ticks()
                time_elapsed = current_time - power_up_timer
                time_left = max(0, (POWER_UP_TYPES[active_power_up["type"]]["duration"] - time_elapsed) // 1000)

                if time_elapsed > POWER_UP_TYPES[active_power_up["type"]]["duration"]:
                    active_power_up = None  # Power-up expired
                    # Reset effects
                    platform_speed = original_platform_speed
                    jump_strength = original_jump_strength
                    invincible = False
            else:
                time_left = 0  # No active power-up

            # Game over condition (only check if not invincible)
            if player_y > SCREEN_HEIGHT and not invincible:
                # Update high score if current score is higher
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                if game_over_screen(score, high_score):  # Restart the game
                    return True
                else:  # Exit the game
                    running = False

            # Update platforms with difficulty-based speed
            for platform in platforms:
                platform.y += platform_speed
                if platform.y > SCREEN_HEIGHT:
                    platform.y = -20
                    platform.x = random.randint(0, SCREEN_WIDTH - platform.width)

            # Draw elements
            # Change player color if invincible
            if invincible:
                pygame.draw.rect(screen, RED, (player_x, player_y, 50, 50))  # Red when invincible
            else:
                pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))  # Normal color

            for platform in platforms:
                pygame.draw.rect(screen, GREEN, platform)

            # Draw power-up
            pygame.draw.rect(screen, power_up["color"], power_up["rect"])

            # Display score and high score
            score_text = small_font.render(f"Score: {score}", True, WHITE)
            high_score_text = small_font.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 40))

            # Display active power-up and timer
            if active_power_up:
                power_up_text = small_font.render(f"Active: {active_power_up['type']} ({time_left}s)", True, WHITE)
                screen.blit(power_up_text, (10, 70))

        if not game_started:
            start_text = small_font.render("Click to Start Jumping", True, WHITE)
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

# Main program
current_screen = "home"
selected_difficulty = "medium"
platforms = generate_platforms(5)  # Default medium difficulty
high_score = load_high_score()  # Load high score at start

while True:
    if current_screen == "home":
        result = home_screen(high_score)
        if result == "start":
            current_screen = "game"
        elif result == "difficulty":
            current_screen = "difficulty"
        else:
            break

    elif current_screen == "difficulty":
        difficulty = difficulty_screen()
        if difficulty == "easy":
            selected_difficulty = "easy"
            platforms = generate_platforms(10)  # More platforms
        elif difficulty == "medium":
            selected_difficulty = "medium"
            platforms = generate_platforms(5)   # Default
        elif difficulty == "hard":
            selected_difficulty = "hard"
            platforms = generate_platforms(3)   # Fewer platforms
        current_screen = "home"

    elif current_screen == "game":
        if game_loop(platforms, selected_difficulty):
            current_screen = "home"
        else:
            break

# Quit Pygame
pygame.quit()
