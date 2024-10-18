#######Functions of game program snips

def place_player_and_enemy(map_data, player_symbol='P', enemy_symbol='E'):
    """Place the player and enemy randomly in the map"""
    empty_tiles = [(x, y) for y, row in enumerate(map_data) for x, tile in enumerate(row) if tile == '.']
    
    if len(empty_tiles) < 2:
        raise ValueError("Not enough empty tiles to place player and enemy.")
    
    # Randomly select a position for the player and enemy
    player_position = random.choice(empty_tiles)
    empty_tiles.remove(player_position)
    enemy_position = random.choice(empty_tiles)
    
    # Place them on the map
    map_data[player_position[1]][player_position[0]] = player_symbol
    map_data[enemy_position[1]][enemy_position[0]] = enemy_symbol
    
    return map_data

# Modify the map to place the player and enemy
map_data = place_player_and_enemy(map_data)



map_data = """
WWWWWWWWWW
W........W
W.W.W.W..W
W.WE.WE..W
W........W
WWWWWWWWWW
"""

def load_map_from_string(map_string):
    """Load the map from a string representation"""
    return [list(line) for line in map_string.strip().split('\n')]

# Load the map from the docstring
map_grid = load_map_from_string(map_data)

# The rest of your Pygame code would remain the same as in the previous example



import pygame

def load_map_from_file(filename='generated_map.txt'):
    """Load the map from a text file"""
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

def draw_map(screen, map_data, tile_size):
    """Draw the map on the screen using Pygame"""
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 'W':  # Wall
                pygame.draw.rect(screen, (0, 0, 255), (x * tile_size, y * tile_size, tile_size, tile_size))
            elif cell == 'E':  # Enemy
                pygame.draw.rect(screen, (255, 0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
            else:  # Floor
                pygame.draw.rect(screen, (200, 200, 200), (x * tile_size, y * tile_size, tile_size, tile_size))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 400))

# Load and draw the map
tile_size = 40
map_data = load_map_from_file()

running = True
while running:
    screen.fill((0, 0, 0))
    draw_map(screen, map_data, tile_size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()




import random

def generate_map(width, height):
    """Generate a simple random map with walls (W), floors (.) and enemies (E)"""
    map_data = []
    for y in range(height):
        row = []
        for x in range(width):
            cell = random.choice(['.', 'W', 'E'])  # Randomly pick floor, wall, or enemy
            row.append(cell)
        map_data.append(row)
    return map_data

def save_map_to_file(map_data, filename='generated_map.txt'):
    """Save the generated map to a text file"""
    with open(filename, 'w') as f:
        for row in map_data:
            f.write(''.join(row) + '\n')

# Generate and save the map
map_data = generate_map(10, 10)
save_map_to_file(map_data)





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




# player.py
import pygame

class Player:
    def __init__(self, x, y, width, height, velocity):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = velocity
        self.color = (0, 0, 255)  # Blue for the player
    
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)



import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class MapEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Editor")
        
        # Ask for map dimensions
        self.map_width = simpledialog.askinteger("Map Width", "Enter the width of the map:", minvalue=5, maxvalue=50)
        self.map_height = simpledialog.askinteger("Map Height", "Enter the height of the map:", minvalue=5, maxvalue=50)
        
        # Create initial map and display it
        self.initial_map = self.create_map(self.map_width, self.map_height)
        
        # Create Text widget for editing map
        self.map_text = tk.Text(self.root, width=self.map_width, height=self.map_height, font=("Courier", 12), wrap="none")
        self.map_text.pack()
        self.map_text.insert("1.0", self.initial_map)
        
        # Buttons for saving, loading, generating random map, and clearing
        self.create_buttons()
    
    def create_buttons(self):
        # Save and generate Pygame code
        save_button = tk.Button(self.root, text="Save Map and Generate Code", command=self.save_map_and_code)
        save_button.pack(pady=5)
        
        # Load saved map
        load_button = tk.Button(self.root, text="Load Saved Map", command=self.load_map)
        load_button.pack(pady=5)
        
        # Generate random map
        random_button = tk.Button(self.root, text="Generate Random Map", command=self.generate_random_map)
        random_button.pack(pady=5)
        
        # Clear the map editor
        clear_button = tk.Button(self.root, text="Clear Map", command=self.clear_map)
        clear_button.pack(pady=5)
    
    def create_map(self, width, height):
        """Create a simple initial map with walls."""
        map_grid = []
        for _ in range(height):
            map_grid.append(" " * width)
        map_grid[0] = "w" * width
        map_grid[-1] = "w" * width
        for i in range(1, height - 1):
            map_grid[i] = "w" + " " * (width - 2) + "w"
        return "\n".join(map_grid)
    
    def generate_random_map(self):
        """Generate a random map with 'w', 's', and ' '."""
        random_map = []
        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                if y == 0 or y == self.map_height - 1 or x == 0 or x == self.map_width - 1:
                    row.append("w")  # Walls around the border
                else:
                    row.append(random.choice(["w", "s", " "]))  # Random wall, space, or special tile
            random_map.append("".join(row))
        self.map_text.delete("1.0", tk.END)
        self.map_text.insert("1.0", "\n".join(random_map))
    
    def clear_map(self):
        """Clear the map in the Text widget."""
        self.map_text.delete("1.0", tk.END)
    
    def save_map_and_code(self):
        """Save the map and generate Pygame code."""
        map_str = self.map_text.get("1.0", tk.END).strip()
        pygame_code = self.generate_pygame_code(map_str)
        
        # Save the map to a file
        with open("saved_map.txt", "w") as f:
            f.write(map_str)
        
        # Save the generated Pygame code
        with open("generated_map_code.py", "w") as f:
            f.write(pygame_code)
        
        messagebox.showinfo("Saved", "Map and Pygame code saved successfully!")
    
    def load_map(self):
        """Load the saved map into the Text widget."""
        try:
            with open("saved_map.txt", "r") as f:
                map_str = f.read()
            self.map_text.delete("1.0", tk.END)
            self.map_text.insert("1.0", map_str)
        except FileNotFoundError:
            messagebox.showwarning("Error", "No saved map found!")
    
    def generate_pygame_code(self, map_str):
        """Generate the Pygame code based on the map."""
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

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    editor = MapEditor(root)
    root.mainloop()
import pygame
from pygame.locals import *

def map_to_list(map_str):
    map_lines = map_str.splitlines()
    return [list(line) for line in map_lines]

map_str = """wwwwww
w    w
w    w
wwwwww"""
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

