# main_game.py
import pygame
from player import Player
from enemy import Enemy

# Initialize pygame
pygame.init()

# Game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Player vs Enemy")

# Game clock
clock = pygame.time.Clock()

# Create player and enemy
player = Player(x=50, y=50, width=40, height=40, velocity=5)
enemy = Enemy(x=700, y=500, width=40, height=40, velocity=3)

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Fill screen with white
    keys = pygame.key.get_pressed()
    
    # Move player and enemy
    player.move(keys)
    enemy.move_towards_player(player.rect)
    
    # Draw player and enemy
    player.draw(screen)
    enemy.draw(screen)
    
    # Check collision
    if player.rect.colliderect(enemy.rect):
        print("Game Over: The enemy hit the player!")
        running = False  # End game when enemy collides with player
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
