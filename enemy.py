# enemy.py
import pygame

class Enemy:
    def __init__(self, x, y, width, height, velocity):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = velocity
        self.color = (255, 0, 0)  # Red for the enemy
    
    def move_towards_player(self, player_rect):
        # Basic AI to move towards the player
        if self.rect.x < player_rect.x:
            self.rect.x += self.velocity
        if self.rect.x > player_rect.x:
            self.rect.x -= self.velocity
        if self.rect.y < player_rect.y:
            self.rect.y += self.velocity
        if self.rect.y > player_rect.y:
            self.rect.y -= self.velocity
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
