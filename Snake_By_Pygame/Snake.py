import pygame
import random
import time

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 12

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.score = 0
        self.color = GREEN
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x) % GRID_WIDTH
        new_y = (head_y + dir_y) % GRID_HEIGHT
        
        # Check if snake hits itself
        if (new_x, new_y) in self.positions[1:]:
            return False  # Game over
            
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return True  # Game continues
    
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.score = 0
    
    def render(self, surface):
        for i, (x, y) in enumerate(self.positions):
            # Draw head differently
            if i == 0:
                pygame.draw.rect(surface, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            else:
                pygame.draw.rect(surface, self.color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        x, y = self.position
        pygame.draw.rect(surface, self.color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BLACK, rect, 1)

def show_game_over(surface, score):
    font = pygame.font.SysFont('arial', 36)
    text = font.render(f"Game Over! Score: {score}", True, RED)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    
    restart_font = pygame.font.SysFont('arial', 24)
    restart_text = restart_font.render("Press SPACE to play again", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    
    surface.blit(text, text_rect)
    surface.blit(restart_text, restart_rect)
    pygame.display.update()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT
        
        if not game_over:
            # Update game state
            if not snake.update():
                game_over = True
            
            # Check if snake eats food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()
                # Make sure food doesn't appear on snake
                while food.position in snake.positions:
                    food.randomize_position()
            
            # Draw everything
            screen.fill(BLACK)
            draw_grid(screen)
            snake.render(screen)
            food.render(screen)
            
            # Display score
            font = pygame.font.SysFont('arial', 20)
            score_text = font.render(f"Score: {snake.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            pygame.display.update()
        else:
            show_game_over(screen, snake.score)
        
        clock.tick(FPS)

if __name__ == "__main__":
    main()