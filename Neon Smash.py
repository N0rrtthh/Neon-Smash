import pygame
import random

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_COLOR = (0, 255, 0)
BALL_RADIUS = 10
BALL_COLOR = (255, 0, 0)
BALL_SPEED = 3
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 20
BLOCK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
FPS = 60
BUTTON_RADIUS = 15

# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Neon Smash!")
clock = pygame.time.Clock()

title_colors = [(255, 255, 0),(255, 20, 147), (0, 255, 255), (0, 255, 0)]

# Game objects
paddle = pygame.Rect((WINDOW_WIDTH - PADDLE_WIDTH) // 2, WINDOW_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = random.choice([-1, 1]) * BALL_SPEED
ball_speed_y = -BALL_SPEED
blocks = []

block_total_width = 10 * BLOCK_WIDTH + 9 * 10  # Total width of all blocks and spacing
block_total_height = 3 * BLOCK_HEIGHT + 2 * 10  # Total height of all blocks and spacing

# Calculate offsets to center blocks horizontally and vertically
block_offset_x = (WINDOW_WIDTH - block_total_width) // 2
block_offset_y = 50

for row in range(3):
    for col in range(10):
        block = pygame.Rect(
            block_offset_x + col * (BLOCK_WIDTH + 10),
            block_offset_y + row * (BLOCK_HEIGHT + 10),
            BLOCK_WIDTH,
            BLOCK_HEIGHT
        )
        blocks.append(block)

score = 0
game_over = False

# Title screen variables
title_font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 36)
user_input = ""
is_typing = False

# Function to draw rounded rectangle
def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    
# Ranking variables
ranking_font = pygame.font.Font(None, 24)
ranking_scores = []

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

# Load ranking scores from file
def load_scores():
    ranking_scores.clear()
    try:
        with open("scores.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    split_line = line.split(":")
                    if len(split_line) == 2:
                        username, score = split_line
                        ranking_scores.append((username, int(score)))
    except FileNotFoundError:
        print("Scores file not found. Starting with an empty ranking.")

# Save ranking scores to file
def save_scores():
    with open("scores.txt", "w") as file:
        for username, score in ranking_scores:
            file.write(f"{username}:{score}\n")

# Function to reset the game
def reset_game():
    global ball_speed_x, ball_speed_y, score, level, blocks, game_over
    ball.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    ball_speed_x = random.choice([-1, 1]) * BALL_SPEED
    ball_speed_y = -BALL_SPEED
    score = 0
    level = 1
    blocks = []
    for row in range(3):
        for col in range(10):
            block = pygame.Rect(
                block_offset_x + col * (BLOCK_WIDTH + 10),
                block_offset_y + row * (BLOCK_HEIGHT + 10),
                BLOCK_WIDTH,
                BLOCK_HEIGHT
            )
            blocks.append(block)
    game_over = False

# Reset the game initially
reset_game()

# Function to display the scoreboard
def display_scoreboard(scores=None):
    if scores is None:
        load_scores()
        scores = get_top_scores(ranking_scores)

    window.fill((0, 0, 0))
    draw_text("LEADERBOARD", button_font, (255, 255, 255), WINDOW_WIDTH // 2, 100)
    y = 200

    # Display ranking scores
    for i, (username, score) in enumerate(scores):
        score_text = str(score)
        name_text = username
        score_text_width = button_font.size(score_text)[0]
        name_text_width = button_font.size(name_text)[0]
        draw_text(name_text  + ":", button_font, (255, 255, 255), WINDOW_WIDTH // 2 - (name_text_width + score_text_width) // 2, y)
        draw_text(score_text, button_font, (255, 255, 255), WINDOW_WIDTH // 2 + (name_text_width + score_text_width) // 2, y)
        y += 50

    # Draw back button
    back_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100, 200, 50)
    draw_rounded_rect(window, back_button, (255, 0, 0), BUTTON_RADIUS)
    draw_text("Back", button_font, (255, 255, 255), back_button.centerx, back_button.centery)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return

        clock.tick(FPS)

# Function to get the top 5 scores
def get_top_scores(scores):
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_scores = sorted_scores[:5]
    return top_scores

# Load ranking scores from file
load_scores()


# Reset game variables
reset_game()
user_input = ""
game_started = False
title_screen = True

# Define restart button
restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100, 200, 50)

# Title screen loop
title_screen = True
game_started = False
clear_leaderboards = False
while True:
    while title_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    if user_input != "":
                        game_started = True
                        title_screen = False
                        is_typing = False
                elif clear_leaderboards_button.collidepoint(event.pos):
                    ranking_scores.clear()
                    save_scores()  
                    clear_leaderboards = True

                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                elif input_box.collidepoint(event.pos):
                    is_typing = True
                elif scoreboard_button.collidepoint(event.pos):
                    top_scores = get_top_scores(ranking_scores)
                    display_scoreboard(top_scores)
                elif restart_button.collidepoint(event.pos):
                    reset_game()
                    game_started = True
                    title_screen = False
                else:
                    is_typing = False


            elif event.type == pygame.KEYDOWN:
                if is_typing:
                    if event.key == pygame.K_RETURN:
                        is_typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

        # Load background image
        background_image = pygame.image.load("background.png")
        # Scale the image to fit the window size
        background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # Draw the background image on the window
        window.blit(background_image, (0, 0))


        # Draw title text
        title_font = pygame.font.Font(None, 100)
        title_text = "NEON SMASH!"
        char_width = 50
        title_text_width = title_font.size(title_text)[0]
        title_pos_x = (WINDOW_WIDTH - title_text_width) // 2
        title_pos_y = WINDOW_HEIGHT // 2 - 140
        underline_y = title_pos_y + title_font.get_height() - 30  # Adjust the underline position

        for i, char in enumerate(title_text):
            char_color = title_colors[i % len(title_colors)]
            char_surface = title_font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(title_pos_x + (i * char_width) + char_width // 2, title_pos_y))
            window.blit(char_surface, char_rect)

        # Draw underline under the title
        underline_start = (title_pos_x, underline_y)
        underline_end = (title_pos_x + title_text_width + char_width, underline_y)
        pygame.draw.line(window, (255, 255, 0), underline_start, underline_end, 2)

        # Draw input box
        input_box = pygame.Rect(WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT // 2 - 55, 320, 50)
        pygame.draw.rect(window, (255, 255, 255), input_box, 2)

        # Placeholder text
        placeholder_text = "Insert username here"

        # Trim the user input if it exceeds the width of the input box
        trimmed_user_input = user_input[:15] + "..." if len(user_input) > 15 else user_input

        # Determine which text to display based on user input
        display_text = trimmed_user_input if user_input else placeholder_text

        # Draw user input text
        input_text = button_font.render(display_text, True, (255, 255, 255))
        input_text_rect = input_text.get_rect(center=input_box.center)
        window.blit(input_text, input_text_rect)

        # Draw play button
        play_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 25, 200, 50)
        draw_rounded_rect(window, play_button, (90, 219, 181), BUTTON_RADIUS)
        draw_text("PLAY", button_font, (255, 255, 255), play_button.centerx, play_button.centery)

        # Draw clear leaderboards button
        clear_leaderboards_button = pygame.Rect(WINDOW_WIDTH // 2 - 155, WINDOW_HEIGHT // 2 + 160, 310, 50)
        draw_rounded_rect(window, clear_leaderboards_button, (87, 131, 219), BUTTON_RADIUS)
        draw_text("CLEAR LEADERBOARD", button_font, (255, 255, 255), clear_leaderboards_button.centerx, clear_leaderboards_button.centery)

        # Draw quit button
        quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 230, 200, 50)
        draw_rounded_rect(window, quit_button, (255, 0, 0), BUTTON_RADIUS)
        draw_text("QUIT", button_font, (255, 255, 255), quit_button.centerx, quit_button.centery)

        # Draw scoreboard button
        scoreboard_button = pygame.Rect(WINDOW_WIDTH // 2 - 110, WINDOW_HEIGHT // 2 + 95, 220, 50)
        draw_rounded_rect(window, scoreboard_button, (255, 189, 3), BUTTON_RADIUS)
        draw_text("LEADERBOARD", button_font, (255, 255, 255), scoreboard_button.centerx, scoreboard_button.centery)
        
        pygame.display.flip()
        clock.tick(FPS)

    # Check if the clear leaderboards button was clicked
    if clear_leaderboards:
        # Clear the ranking scores and save empty scores to the file
        ranking_scores.clear()
        save_scores()

    # Load ranking scores from file
    load_scores()

    # Game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if game_started:
            # Update paddle position based on mouse input
            mouse_x = pygame.mouse.get_pos()[0]
            paddle.x = mouse_x - PADDLE_WIDTH // 2

            # Update ball position
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            # Ball collision with walls
            if ball.left <= 0 or ball.right >= WINDOW_WIDTH:
                ball_speed_x *= -1
            if ball.top <= 0:
                ball_speed_y *= -1

            # Ball collision with paddle
            if ball.colliderect(paddle):
                ball_speed_y *= -1

            # Ball collision with blocks
            for block in blocks:
                if ball.colliderect(block):
                    blocks.remove(block)
                    ball_speed_y *= -1
                    score += 10

            # Level completion condition
            if len(blocks) == 0:
                level += 1
                ball_speed_x = random.choice([-1, 1]) * (BALL_SPEED + level)
                ball_speed_y = -(BALL_SPEED + level)
                for row in range(3):
                    for col in range(10):
                        block = pygame.Rect(
                            block_offset_x + col * (BLOCK_WIDTH + 10),
                            block_offset_y + row * (BLOCK_HEIGHT + 10),
                            BLOCK_WIDTH,
                            BLOCK_HEIGHT
                        )
                        blocks.append(block)

            # Game over condition
            if ball.top > WINDOW_HEIGHT:
                game_over = True

        # Clear the window
        window.fill((0, 0, 0))

        if game_started:
            # Draw game objects
            pygame.draw.rect(window, PADDLE_COLOR, paddle)
            pygame.draw.circle(window, BALL_COLOR, (ball.x, ball.y), BALL_RADIUS)
            for i, block in enumerate(blocks):
                pygame.draw.rect(window, BLOCK_COLORS[i % len(BLOCK_COLORS)], block)

            level_font = pygame.font.Font(None, 30)

            # Draw score and level text
            draw_text("Score: " + str(score), button_font, (255, 255, 255), 70, 20)
            draw_text("Level: " + str(level), level_font, (255, 255, 255), WINDOW_WIDTH - 70, 20)

            # Update the display
            pygame.display.flip()

        else:
            # Ranking screen
            window.fill((0, 0, 0))

            # Sort scores in descending order
            ranking_scores.append((user_input, score))
            ranking_scores.sort(key=lambda x: x[1], reverse=True)

            # Draw ranking text
            draw_text("Ranking", title_font, (255, 255, 255), WINDOW_WIDTH // 2, 50)

            # Draw scores
            for i, (username, score) in enumerate(ranking_scores):
                ranking_text = ranking_font.render(f"{i + 1}. {username}: {score}", True, (255, 255, 255))
                window.blit(ranking_text, (WINDOW_WIDTH // 2 - ranking_text.get_width() // 2, 150 + i * 30))

            # Draw restart button
            restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100, 200, 50)
            draw_rounded_rect(window, restart_button, (0, 255, 0), BUTTON_RADIUS)
            draw_text("Restart", button_font, (255, 255, 255), restart_button.centerx, restart_button.centery)

            pygame.display.flip()

        # Control the game speed
        clock.tick(FPS)

    # Game over screen
    window.fill((0, 0, 0))
    result_text = button_font.render("Game Over! Your score: " + str(score), True, (255, 255, 255))
    window.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, WINDOW_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

    # Add the current user's score to the ranking_scores list
    ranking_scores.append((user_input, score))

    # Save ranking scores to file
    save_scores()

    # Display top 5 ranking scores
    window.fill((0, 0, 0))
    draw_text("Ranking", title_font, (255, 255, 255), WINDOW_WIDTH // 2, 50)

    # Sort scores in descending order
    ranking_scores.sort(key=lambda x: x[1], reverse=True)

    # Display top 5 ranking scores
    top_scores = ranking_scores[:5]
    line_spacing = 55
    for i, (username, score) in enumerate(top_scores):
        ranking_font = pygame.font.Font(None, 40)
        ranking_text = ranking_font.render(f"{i + 1}.{username}: {score}", True, (255, 255, 255))
        text_width = ranking_text.get_width()
        text_height = ranking_text.get_height()
        text_x = WINDOW_WIDTH // 2 - text_width // 2
        text_y = 150 + i * line_spacing
        window.blit(ranking_text, (text_x, text_y))

    # Draw restart button
    restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100, 200, 50)
    draw_rounded_rect(window, restart_button, (0, 255, 0), BUTTON_RADIUS)
    draw_text("Restart", button_font, (255, 255, 255), restart_button.centerx, restart_button.centery)

    pygame.display.flip()

    # Reset game variables
    reset_game()
    user_input = ""
    game_started = False
    title_screen = True

    while title_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    # Reset game variables
                    reset_game()
                    game_started = True
                    title_screen = False

        # Control the game speed
        clock.tick(FPS)

    title_screen = True