import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog,Scrollbar
from PIL import Image, ImageTk
import os
from datetime import datetime
import time

Image.MAX_IMAGE_PIXELS = None


class ScrollableNotebook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.title("Pygame Tools Suite")
        self.current_path = tk.StringVar(value=os.getcwd())

        # Create a frame for the notebook and scrollbar
        notebook_frame = tk.Frame(self, width=600, height=600)
        notebook_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")

        # Configure the grid to expand the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(notebook_frame, width=600, height=600)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar to the frame
        scrollbar = ttk.Scrollbar(notebook_frame, orient="horizontal", command=self.canvas.xview)
        scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(xscrollcommand=scrollbar.set)

        # Configure the notebook frame grid
        notebook_frame.grid_rowconfigure(0, weight=1)
        notebook_frame.grid_columnconfigure(0, weight=1)

        # Create a frame inside the canvas to hold the notebook
        notebook_frame_inside = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=notebook_frame_inside, anchor='nw')

        # Create the notebook
        self.notebook = ttk.Notebook(notebook_frame_inside)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        notebook_frame_inside.bind('<Configure>', self.on_configure)

        # Create the path entry and button on the first tab
        self.f0 = self.add_tab("Title Page")
        ttk.Label(self.f0, text="A Suite of Pygame Tools").grid(row=0, column=0, pady=10)
        ttk.Label(self.f0, text="Directory Path:").grid(row=1, column=0, sticky=tk.W, padx=10)
        self.path_entry = ttk.Entry(self.f0, textvariable=self.current_path, width=50)
        self.path_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10)
        self.browse_button = ttk.Button(self.f0, text="Browse", command=self.select_directory)
        self.browse_button.grid(row=1, column=2, padx=10)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_tab(self, title, **kwargs):
        frame = ttk.Frame(self.notebook, **kwargs)
        self.notebook.add(frame, text=title)
        return frame

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.current_path.set(directory)

    def get_current_path(self):
        return self.current_path.get()

    def select_file(self, filetypes=[("All Files", "*.*")]):
        return filedialog.askopenfilename(filetypes=filetypes)


class CommonFileDialogMixin:
    def __init__(self, notebook):
        self.notebook = notebook

    def select_file(self, filetypes=[("All Files", "*.*")]):
        return self.notebook.select_file(filetypes=filetypes)

    def select_directory(self):
        return self.notebook.select_directory()

    def get_current_path(self):
        return self.notebook.get_current_path()


class ImageBrowser(CommonFileDialogMixin):
    def __init__(self, parent, notebook):
        super().__init__(notebook)
        self.parent = parent
        self.area = (700, 500)
        self.path = self.get_current_path()

        self.btfrm = tk.Frame(self.parent)
        self.btfrm.grid(row=0, column=0)

        self.treefrm = tk.Frame(self.parent)
        self.treefrm.grid(row=3, column=0)

        self.tree = ttk.Treeview(self.treefrm, columns=("Size", "Type", "Modified"))
        self.tree.heading("#0", text="File Name", command=lambda: self.treeview_sort_column("#0", False))
        self.tree.heading("Size", text="Size (KB)", command=lambda: self.treeview_sort_column("Size", False))
        self.tree.heading("Type", text="Type", command=lambda: self.treeview_sort_column("Type", False))
        self.tree.heading("Modified", text="Last Modified", command=lambda: self.treeview_sort_column("Modified", False))

        self.tree.grid(row=0, column=0, rowspan=15, sticky="nswe")
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.sc = ttk.Scrollbar(self.treefrm, orient=tk.VERTICAL, command=self.tree.yview)
        self.sc.grid(row=0, rowspan=15, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.sc.set)

        self.canfrm = tk.Frame(self.parent)
        self.canfrm.grid(row=3, column=2)

        self.canvas = tk.Canvas(self.canfrm, height=self.area[1], width=self.area[0], bg="black", bd=10, relief="ridge")
        self.canvas.grid(row=2, column=1)
        txt = """
        0                             !
                    No Image
        """
        self.wt = self.canvas.create_text(self.area[0] / 2 - 270, self.area[1] / 2, text=txt, font=("", 30), fill="white")
        self.new_dir = tk.Button(self.btfrm, text="new dir", bd=2, bg="lavender", command=self.newdirlist)
        self.new_dir.grid(row=1, column=1)
        self.relist = tk.Button(self.btfrm, text="relist", bd=2, bg="lavender", command=self.list_files)
        self.relist.grid(row=1, column=2)
        btn_open = tk.Button(self.btfrm, text="Open New Image", bd=2, command=self.make_image)
        btn_open.grid(row=1, column=3)
        self.status = tk.Label(self.canfrm, text="Image Browser    Current Image: None")
        self.status.grid(row=0, column=1)

        self.list_files()

    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def get_current_image(self):
        if self.loaded_img:
            return self.loaded_img.copy()
        return None

    def list_files(self):
        self.path = self.get_current_path()
        for item in self.tree.get_children():
            self.tree.Scrollbardelete(item)

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        for file in os.listdir(self.path):
            if file.endswith(tuple(image_extensions)):
                file_path = os.path.join(self.path, file)
                file_size = os.path.getsize(file_path) // 1024
                file_type = 'Image' if any(file.endswith(ext) for ext in image_extensions) else 'Other'
                modified_time = time.ctime(os.path.getmtime(file_path))
                self.tree.insert('', 'end', text=file, values=(file_size, file_type, modified_time))

        self.canvas.delete('all')
        self.status["text"] = "Image Browser    Current Image: None"

    def showcontent(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            file_name = self.tree.item(selected_item[0], 'text')
            full_path = os.path.join(self.path, file_name)
            if os.path.isfile(full_path):
                try:
                    self.loaded_img = Image.open(full_path)
                    re = self.loaded_img.resize((700, 500), Image.Resampling.LANCZOS)
                    self.img = ImageTk.PhotoImage(re)
                    self.canvas.delete('all')
                    self.canvas.create_image(self.area[0] / 2 + 10, self.area[1] / 2 + 10, anchor='center', image=self.img)
                    self.status["text"] = "Image Browser   Current Image: " + full_path
                except Exception as e:
                    messagebox.showerror("Error", f"Error loading image: {e}")
                    seScrollbarlf.status["text"] = "Error loading image"
            else:
                messagebox.showinfo("Information", "Selected item is not an image file")
                self.status["text"] = "Selected item is not an image file"

    def newdirlist(self):
        new_path = self.select_directory()
        if new_path:
            try:
                self.path = new_path
                os.chdir(self.path)
                
                self.status["text"] = f"Directory changed to {self.path}"
                   
            except Exception as e:
                messagebox.showerror("Error", f"Error accessing directory: {e}")
        
        self.list_files()                

    def on_select(self, event):
        self.showcontent(event)

    def make_image(self):
        try:
            filetypes = [('PNG files', '*.png'), ('JPEG files', '*.jpg'), ('JPEG files', '*.jpeg'), ('GIF files', '*.gif'), ('BMP files', '*.bmp'), ('All files', '*.*')]
            self.file = self.select_file(filetypes)
            if self.file:
                self.loaded_img = Image.open(self.file)
                re = self.loaded_img.resize((700, 500), Image.Resampling.LANCZOS)
                self.img = ImageTk.PhotoImage(re)
                self.cScrollbaranvas.delete('all')
                self.canvas.create_image(self.area[0] / 2 + 10, self.area[1] / 2 + 10, anchor='center', image=self.img)
                self.status["text"] = "Image Browser Current Image: " + self.file
        except Exception as e:
            print(f"Error loading image: {e}")
            self.status["text"] = "Error loading image"

    def copy_to_edit_tab(self):
        if self.loaded_img:
            photo = ImageTk.PhotoImage(self.loaded_img)
            img.can.create_image(800, 800, image=photo)
            img.can.image = photo


class ImageTileSplitter(CommonFileDialogMixin):
    def __init__(self, parent, notebook):
        super().__init__(notebook)
        self.parent = parent
        self.auto_create_dir = tk.BooleanVar()
        tk.Label(self.parent, text="Image Path:").grid(row=0, column=0)
        self.entry_image_path = tk.Entry(self.parent, width=50)
        self.entry_image_path.grid(row=0, column=1)
        tk.Button(self.parent, text="Browse", command=self.select_image).grid(row=0, column=2)
        tk.Label(self.parent, text="Tile Width:").grid(row=1, column=0)
        self.entry_tile_width = tk.Entry(self.parent)
        self.entry_tile_width.grid(row=1, column=1)
        tk.Label(self.parent, text="Tile Height:").grid(row=2, column=0)
        self.entry_tile_height = tk.Entry(self.parent)
        self.entry_tile_height.grid(row=2, column=1)
        tk.Label(self.parent, text="Output Directory:").grid(row=3, column=0)
        self.entry_output_dir = tk.Entry(self.parent, width=50)
        self.entry_output_dir.grid(row=3, column=1)
        tk.Button(self.parent, text="Browse", command=self.outputdir)
        tk.Checkbutton(self.parent, text="Auto-create Output Directory", variable=self.auto_create_dir).grid(row=4, column=0)
        tk.Button(self.parent, text="Split Image", command=self.split_image).grid(row=4, column=1)


    def outputdir(self):
            
        path = filedialog.askopendirectory()
        
        self.entry_output_dir.insert(0, path)
    def select_image(self):
        file_path = self.select_file()
        if file_path:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, file_path)

    def split_image(self):
        image_path = self.entry_image_path.get()
        tile_width = int(self.entry_tile_width.get())
        tile_height = int(self.entry_tile_height.get())
        output_dir = self.entry_output_dir.get()

        # Ensure all inputs are provided
        if not (image_Scrollbarpath and tile_width and tile_height and output_dir) and not self.auto_create_dir.get():
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            image = Image.open(image_path)
            img_width, img_height = image.size

            if self.auto_create_dir.get():
                output_dir = os.path.join("output_tiles", datetime.now().strftime("%Y%m%d_%H%M%S"))
                os.makedirs(output_dir, exist_ok=True)
            else:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

            tile_number = 0
            for i in range(0, img_width, tile_width):
                for j in range(0, img_height, tile_height):
                    box = (i, j, i + tile_width, j + tile_height)
                    tile = image.crop(box)
                    tile_filename = f'tile_{tile_number}.png'
                    tile.save(os.path.join(output_dir, tile_filename))
                    tile_number += 1

            messagebox.showinfo("Success", f"Image split into {tile_number} tiles successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

            

class ShapeTerrainGenerator(CommonFileDialogMixin):
    def __init__(self, parent, notebook):
        super().__init__(notebook)
        self.parent = parent

        self.main_frame = ttk.Frame(self.parent, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Number of shapes
        ttk.Label(self.main_frame, text="Number of shapes:").grid(row=0, column=0, sticky=tk.W)
        self.num_shapes_entry = ttk.Entry(self.main_frame)
        self.num_shapes_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        # R variation
        ttk.Label(self.main_frame, text="R variation:").grid(row=1, column=0, sticky=tk.W)
        self.r_variation_entry = ttk.Entry(self.main_frame)
        self.r_variation_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # G variation
        ttk.Label(self.main_frame, text="G variation:").grid(row=2, column=0, sticky=tk.W)
        self.g_variation_entry = ttk.Entry(self.main_frame)
        self.g_variation_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        # B variation
        ttk.Label(self.main_frame, text="B variation:").grid(row=3, column=0, sticky=tk.W)
        self.b_variation_entry = ttk.Entry(self.main_frame)
        self.b_variation_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        # Buttons for code generation, open/save, clear, copy/paste
        self.generate_button = ttk.Button(self.main_frame, text="Generate Code", command=self.generate_code)
        self.generate_button.grid(row=4, column=0, columnspan=2)

        self.code_text = scrolledtext.ScrolledText(self.main_frame, width=80, height=20)
        self.code_text.grid(row=5, column=0, columnspan=2)

        # Button frame for extra options
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Add buttons for Clear, Copy, Paste, Open, Save
        ttk.Button(button_frame, text="Clear", command=self.clear_text).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Copy", command=self.copy_text).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Paste", command=self.paste_text).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Open", command=self.open_file).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_file).grid(row=0, column=4, padx=5)

    def generate_code(self):
        try:
            num_shapes = int(self.num_shapes_entry.get())
            r_variation = int(self.r_variation_entry.get())
            g_variation = int(self.g_variation_entry.get())
            b_variation = int(self.b_variation_entry.get())
        except ValueError:
            self.code_text.insert(tk.END, "Please enter valid numbers.\n")
            return

        code = f"""
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
base_color = (100, 150, 200)

def random_color():
    r = max(0, min(255, base_color[0] + random.randint(-{r_variation}, {r_variation})))
    g = max(0, min(255, base_color[1] + random.randint(-{g_variation}, {g_variation})))
    b = max(0, min(255, base_color[2] + random.randint(-{b_variation}, {b_variation})))
    return (r, g, b)

def draw_shapes():
    screen.fill((255, 255, 255))
    for _ in range({num_shapes}):
        color = random_color()
        shape = random.choice(['circle', 'square', 'ellipse', 'triangle', 'polygon'])
        if shape == 'circle':
            pygame.draw.circle(screen, color, (random.randint(0, screen_width), random.randint(0, screen_height)), 20)
        elif shape == 'square':
            rect = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 40, 40)
            pygame.draw.rect(screen, color, rect)
        elif shape == 'ellipse':
            rect = pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 60, 40)
            pygame.draw.ellipse(screen, color, rect)
        elif shape == 'triangle':
            point1 = (random.randint(0, screen_width), random.randint(0, screen_height))
            point2 = (random.randint(0, screen_width), random.randint(0, screen_height))
            point3 = (random.randint(0, screen_width), random.randint(0, screen_height))
            pygame.draw.polygon(screen, color, [point1, point2, point3])
        elif shape == 'polygon':
            points = [(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(6)]
            pygame.draw.polygon(screen, color, points)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_shapes()
    pygame.display.flip()

pygame.quit()
"""
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, code)

    def clear_text(self):
        """Clears the text from the ScrolledText widget."""
        self.code_text.delete(1.0, tk.END)

    def copy_text(self):
        """Copies the selected text from the ScrolledText widget."""
        selected_text = self.code_text.selection_get()
        pyperclip.copy(selected_text)

    def paste_text(self):
        """Pastes the clipboard text into the ScrolledText widget."""
        clipboard_text = pyperclip.paste()
        self.code_text.insert(tk.INSERT, clipboard_text)

    def open_file(self):
        """Opens a .py file and loads its content into the ScrolledText widget."""
        file_path = filedialog.askopenfilename(defaultextension=".py",
                                               filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(tk.END, content)

    def save_file(self):
        """Saves the content of the ScrolledText widget to a .py file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                                 filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.code_text.get(1.0, tk.END)
                file.write(content)
class AnimationGenerator(CommonFileDialogMixin):
    def __init__(self, parent, notebook):
        super().__init__(notebook)
        self.parent = parent
        self.main_frame = ttk.Frame(self.parent, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.main_frame, text="Number of frames:").grid(row=0, column=0, sticky=tk.W)
        self.num_frames_entry = ttk.Entry(self.main_frame)
        self.num_frames_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.main_frame, text="Select Images:").grid(row=1, column=0, sticky=tk.W)
        self.images_listbox = tk.Listbox(self.main_frame, selectmode=tk.MULTIPLE, height=5)
        self.images_listbox.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.load_images_button = ttk.Button(self.main_frame, text="Load Images", command=self.load_images)
        self.load_images_button.grid(row=2, column=1, sticky=(tk.W, tk.E))

        self.generate_button = ttk.Button(self.main_frame, text="Generate Code", command=self.generate_code)
        self.generate_button.grid(row=3, column=0, columnspan=2)

        self.code_text = scrolledtext.ScrolledText(self.main_frame, width=80, height=20)
        self.code_text.grid(row=4, column=0, columnspan=2)

        self.image_paths = []

    def load_images(self):
        filepaths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        for filepath in filepaths:
            self.image_paths.append(filepath)
            self.images_listbox.insert(tk.END, os.path.basename(filepath))

    def generate_code(self):
        try:
            num_frames = int(self.num_frames_entry.get())
        except ValueError:
            self.code_text.insert(tk.END, "Please enter a valid number of frames.\n")
            return

        if not self.image_paths:
            self.code_text.insert(tk.END, "Please load at least one image.\n")
            return

        image_loads = "\n".join([f'images.append(pygame.image.load("{path}"))' for path in self.image_paths])
        code = f"""
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load images
images = []
{image_loads}

# Animation settings
num_frames = {num_frames}
frame_duration = 100  # milliseconds per frame
clock = pygame.time.Clock()

def main():
    running = True
    frame = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        screen.blit(images[frame % len(images)], (100, 100))
        pygame.display.flip()
        
        frame += 1
        clock.tick(1000 // frame_duration)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
"""
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, code)



class ImageMerger(CommonFileDialogMixin):
    def __init__(self, parent, notebook):
        super().__init__(notebook)
        self.parent = parent
        
        self.path_entry = tk.Entry(self.parent, bd=7, width=50)
        self.path_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
       
        self.update_button = tk.Button(self.parent, bd=3, text="Update Directory", command=self.update_directory)
        self.update_button.grid(row=0, column=2, padx=10, pady=10)
        self.file_listbox = tk.Listbox(self.parent, bd=5, selectmode=tk.MULTIPLE, width=50, height=15)
        self.file_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.add_image_button = tk.Button(self.parent, bd=4, text="Add Selected Images", command=self.add_selected_images)
        self.add_image_button.grid(row=2, column=0, padx=10, pady=10)
        self.merge_button = tk.Button(self.parent, bd=6, text="Merge Images", command=self.merge_images)
        self.merge_button.grid(row=2, column=1, padx=10, pady=10)
        self.save_button = tk.Button(self.parent, text="Save Merged Image", command=self.save_merged_image)
        self.save_button.grid(row=2, column=2, padx=10, pady=10)
        self.browse_button = tk.Button(self.parent, bd=5, bg="light blue", text="Browse/Change Directory", command=self.browse_directories)
        self.browse_button.grid(row=0, column=3, padx=10, pady=10)
        self.canvas = tk.Canvas(self.parent, width=800, height=600)
        self.canvas.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self.images = []
        self.merged_image = None
        self.path = os.getcwd()
        self.path_entry.insert(0, self.path)
        self.update_file_list()
    def update_directory(self):
        self.path = self.path_entry.get()
        if os.path.isdir(self.path):
            self.update_file_list()
        else:
            messagebox.showerror("Error", "Invalid directory path.")

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        files = os.listdir(self.path_entry.get())
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                self.file_listbox.insert(tk.END, file)

    def browse_directories(self):
        self.path = filedialog.askdirectory()
        self.file_listbox.delete(0, tk.END)
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(tk.END, self.path)
        os.listdir(self.path)
        for file in self.path:
            print(self.path)
            self.update_directory()
            
                

    def add_selected_images(self):
        selected_files = [self.file_listbox.get(i) for i in self.file_listbox.curselection()]
        for file in selected_files:
            file_path = os.path.join(self.path_entry.get(), file)
            image = Image.open(file_path)
            self.images.append(image)
            self.display_image(image)

    def display_image(self, image):
        tk_image = ImageTk.PhotoImage(image.resize((200, 200)))
        self.canvas.create_image(10 + len(self.images) * 210, 10, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image  # Keep a reference to avoid garbage collection

    def merge_images(self):
        if len(self.images) < 2:
            messagebox.showerror("Error", "Please add at least two images to merge.")
            return

        widths, heights = zip(*(i.size for i in self.images))
        total_width = sum(widths)
        max_height = max(heights)

        self.merged_image = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for image in self.images:
            self.merged_image.paste(image, (x_offset, 0))
            x_offset += image.width

        self.display_merged_image(self.merged_image)

    def display_merged_image(self, image):
        image = image.resize((800, 600))
        tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image  # Keep a reference to avoid garbage collection

    def save_merged_image(self):
        if self.merged_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
            if file_path:
                self.merged_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showerror("Error", "No merged image to save.")


class SpritesheetAnimationGenerator(CommonFileDialogMixin):
    def __init__(self, parent, notebook):
        super().__init__(notebook)
        self.parent = parent
        tk.Label(self.parent, text="Width:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_width = tk.Entry(self.parent)
        self.entry_width.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.parent, text="Height:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_height = tk.Entry(self.parent)
        self.entry_height.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.parent, text="Sheet Width:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_sheet_width = tk.Entry(self.parent)
        self.entry_sheet_width.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.parent, text="Sheet Height:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_sheet_height = tk.Entry(self.parent)
        self.entry_sheet_height.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.parent, text="Number of Frames:").grid(row=4, column=0, padx=10, pady=5)
        self.entry_num_frames = tk.Entry(self.parent)
        self.entry_num_frames.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.parent, text="Spritesheet File:").grid(row=5, column=0, padx=10, pady=5)
        self.entry_file_path = tk.Entry(self.parent, width=50)
        self.entry_file_path.grid(row=5, column=1, padx=10, pady=5)
        self.button_file_path = tk.Button(self.parent, text="Browse", command=self.select_file_path)
        self.button_file_path.grid(row=5, column=2, padx=10, pady=5)

        # Create and place the button to generate the code
        self.button_generate = tk.Button(self.parent, text="Generate Code", command=self.generate_code)
        self.button_generate.grid(row=6, columnspan=3, pady=10)

        # Create a Text widget to display the generated code
        self.text_output = tk.Text(self.parent, width=80, height=20)
        self.text_output.grid(row=7, columnspan=3, padx=10, pady=10)

    def select_file_path(self):
        file_path = self.select_file([("Image files", "*.png;*.jpg;*.jpeg")])
        self.entry_file_path.delete(0, tk.END)
        self.entry_file_path.insert(0, file_path)

    def generate_code(self):
        width = int(self.entry_width.get())
        height = int(self.entry_height.get())
        sheet_width = int(self.entry_sheet_width.get())
        sheet_height = int(self.entry_sheet_height.get())
        num_frames = int(self.entry_num_frames.get())
        file_path = self.entry_file_path.get()

        pygame_code = f"""
import pygame
import sys

pygame.init()

# Screen dimensions
width, height = {width}, {height}
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Spritesheet Animation')

# Load spritesheet
spritesheet = pygame.image.load(r'{file_path}').convert_alpha()

# Frame dimensions
frame_width = {sheet_width} // {num_frames}

# Animation settings
frame_index = 0
clock = pygame.time.Clock()
animation_speed = 10  # Adjust as needed

def get_frame(index):
    x = index * frame_width
    return spritesheet.subsurface(pygame.Rect(x, 0, frame_width, {sheet_height}))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_index = (frame_index + 1) % {num_frames}
    frame = get_frame(frame_index)

    screen.fill((0, 0, 0))
    screen.blit(frame, (0, 0))

    pygame.display.flip()
    clock.tick(animation_speed)

pygame.quit()
sys.exit()
"""
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, pygame_code)

        # Save the generated code to a filede
        epoch_time = int(time.time())
        file_name = f"pygame_code_{epoch_time}.py"
        with open(file_name, "w") as file:
            file.write(pygame_code)
        messagebox.showinfo("Saved", f"Pygame code saved as {file_name}")

class ImageResizerApp:
    def __init__(self, parent, notebook):
        self.parent = parent
        self.notebook = notebook
        self.select_button = tk.Button(self.parent, text="Select Folder and Resize Images", command=self.select_folder)
        self.select_button.grid(row=5,column=5)
    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            resize_factor = simpledialog.askfloat("Resize Factor", "Enter resize factor (e.g., 0.8 for 80%):", minvalue=0.1, maxvalue=1.0)
            if resize_factor:
                self.resize_images(folder_selected, resize_factor)

    def resize_images(self, input_folder, resize_factor):
        epoch_time = str(int(time.time()))
        output_folder = os.path.join(input_folder, f'resized_output_{epoch_time}')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for file in os.listdir(input_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(input_folder, file)
                try:
                    with Image.open(img_path) as img:
                        # Resizing the image
                        new_size = tuple(int(dim * resize_factor) for dim in img.size)
                        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                        # Saving the resized image
                        resized_img.save(os.path.join(output_folder, file))
                        print(f"Resized and saved: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

class SpriteSheetBuilder:
    def __init__(self, parent):
        self.parent = parent
             # Frames
        self.main_frame = ttk.Frame(self.parent, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Widgets
        ttk.Label(self.main_frame, text="Select images to create a sprite sheet:").grid(row=0, column=0, columnspan=2)

        self.select_button = ttk.Button(self.main_frame, text="Select Images", command=self.select_images)
        self.select_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.grid_size_label = ttk.Label(self.main_frame, text="Grid Size (Columns x Rows):")
        self.grid_size_label.grid(row=2, column=0, sticky=tk.W)

        self.columns_entry = ttk.Entry(self.main_frame, width=5)
        self.columns_entry.grid(row=2, column=1, sticky=tk.W)
        self.columns_entry.insert(0, "3")  # Default 3 columns

        self.build_button = ttk.Button(self.main_frame, text="Build Sprite Sheet", command=self.build_sprite_sheet)
        self.build_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.save_button = ttk.Button(self.main_frame, text="Save Sprite Sheet", command=self.save_sprite_sheet)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.save_button.config(state=tk.DISABLED)

        self.preview_button = ttk.Button(self.main_frame, text="Preview Sprite Sheet", command=self.preview_sprite_sheet)
        self.preview_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.preview_button.config(state=tk.DISABLED)

        # Canvas for preview with scrollbars
        self.canvas_frame = ttk.Frame(self.parent)
        self.canvas_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        # Add scrollbars
        self.scroll_x = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky=tk.EW)

        self.scroll_y = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky=tk.NS)

        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Zoom buttons
        self.zoom_in_button = ttk.Button(self.main_frame, text="Zoom In", command=lambda: self.zoom(1.2))
        self.zoom_in_button.grid(row=7, column=0)

        self.zoom_out_button = ttk.Button(self.main_frame, text="Zoom Out", command=lambda: self.zoom(0.8))
        self.zoom_out_button.grid(row=7, column=1)

        self.images = []
        self.sprite_sheet = None
        self.preview_image = None  # To hold the preview image
        self.zoom_level = 1.0  # Track the zoom level

    def select_images(self):
        """Opens a file dialog to select multiple image files."""
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"),("All Files", "*.*")])

        if not file_paths:
            return  # No images selected

        # Load the selected images
        self.images = [Image.open(img_path) for img_path in file_paths]
        messagebox.showinfo("Images Selected", f"{len(self.images)} images selected.")

    def build_sprite_sheet(self):
        """Creates a sprite sheet from the selected images."""
        if not self.images:
            messagebox.showerror("No Images", "Please select images before building the sprite sheet.")
            return

        try:
            columns = int(self.columns_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for columns.")
            return

        # Determine rows based on the number of images and columns
        rows = (len(self.images) + columns - 1) // columns

        # Get the size of the first image to determine the size of each cell in the grid
        img_width, img_height = self.images[0].size

        # Create a new image (sprite sheet) large enough to hold all selected images in the grid
        sprite_width = img_width * columns
        sprite_height = img_height * rows
        self.sprite_sheet = Image.new('RGBA', (sprite_width, sprite_height))

        # Paste each image into the appropriate location in the sprite sheet
        for index, img in enumerate(self.images):
            row, col = divmod(index, columns)
            self.sprite_sheet.paste(img, (col * img_width, row * img_height))

        # Display a success message and enable the save and preview buttons
        messagebox.showinfo("Sprite Sheet Built", "Sprite sheet built successfully.")
        self.save_button.config(state=tk.NORMAL)
        self.preview_button.config(state=tk.NORMAL)

    def save_sprite_sheet(self):
        """Saves the generated sprite sheet to a file."""
        if self.sprite_sheet is None:
            messagebox.showerror("No Sprite Sheet", "Please build a sprite sheet first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")])

        if save_path:
            self.sprite_sheet.save(save_path)
            messagebox.showinfo("Save Successful", f"Sprite sheet saved as {save_path}")

    def preview_sprite_sheet(self):
        """Displays a preview of the generated sprite sheet on the canvas."""
        if self.sprite_sheet is None:
            messagebox.showerror("No Sprite Sheet", "Please build a sprite sheet first.")
            return

        self.update_preview(self.sprite_sheet)

    def update_preview(self, image):
        """Updates the canvas with the provided image."""
        self.preview_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.preview_image, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))  # Update scroll region

    def zoom(self, scale_factor):
        """Zooms in or out the sprite sheet by adjusting the zoom level."""
        if self.sprite_sheet is None:
            messagebox.showerror("No Sprite Sheet", "Please build a sprite sheet first.")
            return

        # Update the zoom level
        self.zoom_level *= scale_factor

        # Resize the image according to the new zoom level
        new_width = int(self.sprite_sheet.width * self.zoom_level)
        new_height = int(self.sprite_sheet.height * self.zoom_level)
        resized_sprite_sheet = self.sprite_sheet.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Update the preview
        self.update_preview(resized_sprite_sheet)














class Standard_Pygame_Code:
    def __init__(self, parent):
        self.parent = parent
        self.snippet_frame = tk.Frame(self.parent)
        self.snippet_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Add multiple snippet buttons
        tk.Button(self.snippet_frame, text="Basic Pygame Setup", command=self.insert_basic_setup).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.snippet_frame, text="Event Handling", command=self.insert_event_handling).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.snippet_frame, text="Drawing Shapes", command=self.insert_drawing_shapes).grid(row=0, column=2, padx=5, pady=5)
        
        # Add ScrolledText for displaying code
        self.txtwidget = scrolledtext.ScrolledText(self.parent, width=80, height=40, font=("Courier", 10))
        self.txtwidget.grid(row=1, column=0, columnspan=3)
        
        # Add buttons to clear, copy, and save the snippet
        button_frame = tk.Frame(self.parent)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        tk.Button(button_frame, text="Clear", command=self.clear_text).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Copy", command=self.copy_text).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Save", command=self.save_snippet).grid(row=0, column=2, padx=5)
        tk.Button(self.snippet_frame, text="sacred_pygame", command=self.insert_event_handling2).grid(row=0, column=4, padx=5, pady=5)

        self.basic_setup_code = '''import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Basic Setup")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()'''

    def insert_basic_setup(self):
        self.txtwidget.insert(tk.END, self.basic_setup_code + "\n\n")

    def insert_event_handling(self):
        event_handling_code = '''for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_SPACE:
        print("Spacebar pressed")'''
        self.txtwidget.insert(tk.END, event_handling_code + "\n\n")
    def insert_event_handling2(self):
        event_handling_code2 = '''for event in pygame.event.get():
if event.type == pg.QUIT:
    done = True
if event.type == pygame.K_ESCAPE:
    done=False
        if event.key == pygame.K_SPACE:
            print("Spacebar pressed")'''
        self.txtwidget.insert(tk.END, event_handling_code2 + "\n\n")
       
    def insert_drawing_shapes(self):
        drawing_shapes_code = '''pygame.draw.rect(screen, (255, 0, 0), (50, 50, 100, 100))
pygame.draw.circle(screen, (0, 255, 0), (400, 300), 50)'''
        self.txtwidget.insert(tk.END, drawing_shapes_code + "\n\n")

    def clear_text(self):
        self.txtwidget.delete(1.0, tk.END)

    def copy_text(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.txtwidget.get(1.0, tk.END))

    def save_snippet(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.txtwidget.get(1.0, tk.END))
            messagebox.showinfo("Saved", "Code snippet saved successfully!")



class TabFrame:
    def __init__(self, notebook):
        self.f0 = notebook.add_tab("Title Page")
        ttk.Label(self.f0, text="A Suite of Pygame Tools").grid(row=1, column=1)
        self.f1 = notebook.add_tab("Image Split")
        ImageTileSplitter(self.f1, notebook)
        self.f2 = notebook.add_tab("Create Shapes")
        ShapeTerrainGenerator(self.f2, notebook)
        self.f3 = notebook.add_tab("Animation")
        AnimationGenerator(self.f3, notebook)
        self.f4 = notebook.add_tab("Image Merger")
        ImageMerger(self.f4, notebook)
        self.f5 = notebook.add_tab("Sprite Animator")
        SpritesheetAnimationGenerator(self.f5, notebook)
        self.f6 = notebook.add_tab("Image Browser")
        ImageBrowser(self.f6, notebook)
        self.f7 = notebook.add_tab("Multi Image Resizer")
        ImageResizerApp(self.f7, notebook)
        self.f8 = notebook.add_tab("Spritesheet Builder")
        SpriteSheetBuilder(self.f8)
        
        self.f9 = notebook.add_tab("Code_Snips")
        Standard_Pygame_Code(self.f9)
        
if __name__ == '__main__':
    nb = ScrollableNotebook()
    TabFrame(nb)
    nb.mainloop()
