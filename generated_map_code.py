
import pygame
from pygame.locals import *

def map_to_list(map_str):
    map_lines = map_str.splitlines()
    return [list(line) for line in map_lines]

map_str = """wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
w                               w
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"""
game_map = map_to_list(map_str)

def display_tiles(screen, game_map, tile_size=32):
    colors = {
        "w": (255, 0, 0),  # Red for walls
        " ": (0, 255, 0),  # Green for empty space
        "s": (0, 0, 255),  # Blue for special tiles
    }
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            color = colors.get(tile, (0, 0, 0))
            pygame.draw.rect(screen, color, (x * tile_size, y * tile_size, tile_size, tile_size))

pygame.init()
screen = pygame.display.set_mode((len(game_map[0]) * 32, len(game_map) * 32))
pygame.display.set_caption("Map Display")

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))
    display_tiles(screen, game_map)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
