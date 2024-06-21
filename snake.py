import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Snake and food size
BLOCK_SIZE = 20

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "RIGHT"

    def move(self):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE
        self.body.insert(0, (x, y))

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):
        x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        return x, y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def game_over():
    font = pygame.font.SysFont(None, 50)
    text = font.render("Game Over! Press Q to Quit or R to Restart", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 25))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "QUIT"
                if event.key == pygame.K_r:
                    return "RESTART"

def main():
    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        snake.move()

        # Check for collision with food
        if snake.body[0] == food.position:
            snake.grow()
            food.position = food.randomize_position()
            score += 1

        # Check for collision with walls
        if (snake.body[0][0] < 0 or snake.body[0][0] >= SCREEN_WIDTH or
            snake.body[0][1] < 0 or snake.body[0][1] >= SCREEN_HEIGHT):
            action = game_over()
            if action == "QUIT":
                return
            elif action == "RESTART":
                return main()

        # Check for collision with self
        if snake.body[0] in snake.body[1:]:
            action = game_over()
            if action == "QUIT":
                return
            elif action == "RESTART":
                return main()

        screen.fill(BLACK)
        snake.draw()
        food.draw()

        # Display score
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (5, 5))

        pygame.display.flip()
        clock.tick(7)  # 10 Controls game speed

if __name__ == "__main__":
    main()
    pygame.quit()