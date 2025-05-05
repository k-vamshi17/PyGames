import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Ball")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_radius = 20
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = random.choice([-4, -3, 3, 4])
ball_speed_y = random.choice([-4, -3, 3, 4])

# Paddle properties
paddle_width = 100
paddle_height = 15
paddle_x = (SCREEN_WIDTH - paddle_width) // 2
paddle_y = SCREEN_HEIGHT - 40
paddle_speed = 8

# Score
score = 0
font = pygame.font.Font(None, 36)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Game logic
    # Move the paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - paddle_width:
        paddle_x += paddle_speed
    
    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Ball collision with walls
    if ball_x <= ball_radius or ball_x >= SCREEN_WIDTH - ball_radius:
        ball_speed_x = -ball_speed_x
    if ball_y <= ball_radius:
        ball_speed_y = -ball_speed_y
    
    # Ball collision with paddle
    if (ball_y + ball_radius >= paddle_y and 
        ball_x >= paddle_x and 
        ball_x <= paddle_x + paddle_width):
        ball_speed_y = -ball_speed_y
        score += 1
    
    # Ball out of bounds (game over)
    if ball_y > SCREEN_HEIGHT:
        running = False
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw the ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    
    # Draw the paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    
    # Draw the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(FPS)

# Game over message
game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
pygame.display.flip()
pygame.time.wait(3000)

# Clean up
pygame.quit()
sys.exit()