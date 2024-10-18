import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to generate map
def create_map(width, height):
    map_grid = []
    for _ in range(height):
        map_grid.append([" "] * width)
    map_grid[0] = ["w"] * width
    map_grid[-1] = ["w"] * width
    for i in range(1, height - 1):
        map_grid[i][0] = "w"
        map_grid[i][-1] = "w"
    return map_grid

# Function to display the map in the console
def display_map(map_grid):
    for row in map_grid:
        print("".join(row))

# Function to modify a specific tile in the map
def modify_map(map_grid, x, y, tile):
    if 0 <= y < len(map_grid) and 0 <= x < len(map_grid[0]):
        map_grid[y][x] = tile
    else:
        print("Invalid position")

# Function to generate pygame code
def generate_pygame_code(map_grid):
    map_str = "\n".join(["".join(row) for row in map_grid])
    code_template = f'''
import pygame
from pygame.locals import *

def map_to_list(map_str):
    map_lines = map_str.splitlines()
    return [list(line) for line in map_lines]

map_str = """{map_str}"""
game_map = map_to_list(map_str)

def display_tiles(screen, game_map, tile_size=32):
    colors = {{
        "w": (255, 0, 0),  # Red for walls
        " ": (0, 255, 0),  # Green for empty space
        "s": (0, 0, 255),  # Blue for special tiles
    }}
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
'''
    return code_template

# GUI for setting map dimensions and generating the code
root = tk.Tk()
root.withdraw()  # Hide the root window

# Get map dimensions
map_width = simpledialog.askinteger("Map Width", "Enter the width of the map:", minvalue=5, maxvalue=50)
map_height = simpledialog.askinteger("Map Height", "Enter the height of the map:", minvalue=5, maxvalue=50)

# Create the map
game_map = create_map(map_width, map_height)

# Display the initial map
print("Initial Map:")
display_map(game_map)

# Modify the map in specific positions
while True:
    modify = messagebox.askyesno("Modify Map", "Do you want to modify a tile?")
    if not modify:
        break
    x = simpledialog.askinteger("Tile X", "Enter the X position of the tile:", minvalue=0, maxvalue=map_width - 1)
    y = simpledialog.askinteger("Tile Y", "Enter the Y position of the tile:", minvalue=0, maxvalue=map_height - 1)
    tile = simpledialog.askstring("Tile", "Enter the tile character (e.g., 'w', 's', ' '):")
    modify_map(game_map, x, y, tile)
    print("Updated Map:")
    display_map(game_map)

# Generate and display Pygame code
pygame_code = generate_pygame_code(game_map)
print("\nGenerated Pygame Code:\n")
print(pygame_code)

# Optionally, save the generated code to a file
with open("generated_map_code.py", "w") as f:
    f.write(pygame_code)

messagebox.showinfo("Success", "Pygame code generated and saved as 'generated_map_code.py'")
