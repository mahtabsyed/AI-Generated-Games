import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 150, 15 # 100, 15
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
BALL_SIZE = 15
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_dx, ball_dy = 5, -5

# Bricks
BRICK_WIDTH, BRICK_HEIGHT = 70, 30  # 70, 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE]

bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append((brick, BRICK_COLORS[row]))

# Game variables
clock = pygame.time.Clock()
score = 0
lives = 3
font = pygame.font.Font(None, 36)

def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    return 5 * random.choice((1, -1)), -2 # -5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 12 # 7
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += 12 # 7

    # Move the ball
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx *= -1
    if ball.top <= 0:
        ball_dy *= -1
    if ball.bottom >= HEIGHT:
        lives -= 1
        if lives > 0:
            ball_dx, ball_dy = reset_ball()
        else:
            running = False

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_dy *= -1
        # Adjust angle based on where ball hits paddle
        ball_dx += (ball.centerx - paddle.centerx) / 10
        ball_dx = max(min(ball_dx, 5), -5)  # 8, -8 Limit horizontal speed

    # Ball collision with bricks
    for brick, color in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove((brick, color))
            ball_dy *= -1
            score += 10
            break

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    pygame.display.flip()
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
game_over_text = font.render("GAME OVER", True, WHITE)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)
pygame.quit()