import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import time
import csv
import os



class ImageClickApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Click Logger")

        self.label = tk.Label(self.root, text="Select a folder to save and an background image to start")
        self.label.pack()

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
        
        self.folder_button = tk.Button(self.root, text="Select Folder", command=self.choose_folder)
        self.folder_button.pack()
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.log_file_women = "click_log_women.csv"
        self.log_file_men = "click_log_men.csv"

        # Initialize lists for previous clicks
        self.previous_clicks_women = []
        self.previous_clicks_men = []
        
        # Initialize image variables
        self.image_heel = None
        self.image_sneaker = None
        self.image_woman = None
        self.image_man = None
        self.tk_image_heel = None
        self.tk_image_sneaker = None
        self.tk_image_woman = None
        self.tk_image_man = None
        
        # Load the small images for icons
        self.load_icons()

        self.image = None
        self.tk_image = None
        self.save_folder = None

        # Bind the "s" key to save the canvas
        self.root.bind("s", self.save_canvas)

    def load_icons(self):
        """Load small images to replace emojis."""
        try:
            # Load images and resize them
            self.image_heel = Image.open("icons/heel.png").resize((15, 15), Image.Resampling.LANCZOS)
            self.image_sneaker = Image.open("icons/sneaker.png").resize((15, 15), Image.Resampling.LANCZOS)
            self.image_woman = Image.open("icons/women1.PNG").resize((120, 120), Image.Resampling.LANCZOS)
            self.image_man = Image.open("icons/man1.PNG").resize((120, 120), Image.Resampling.LANCZOS)
            self.image_woman2 = Image.open("icons/women2.PNG").resize((120, 120), Image.Resampling.LANCZOS)
            self.image_man2 = Image.open("icons/man2.PNG").resize((120, 120), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            self.tk_image_heel = ImageTk.PhotoImage(self.image_heel)
            self.tk_image_sneaker = ImageTk.PhotoImage(self.image_sneaker)
            self.tk_image_woman = ImageTk.PhotoImage(self.image_woman)
            self.tk_image_man = ImageTk.PhotoImage(self.image_man)

            self.tk_image_woman2 = ImageTk.PhotoImage(self.image_woman2)
            self.tk_image_man2 = ImageTk.PhotoImage(self.image_man2)

        except Exception as e:
            print(f"Error loading icons: {e}")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")])
        if not file_path:
            return

        self.image = Image.open(file_path)

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the new size while maintaining the aspect ratio
        aspect_ratio = self.image.width / self.image.height
        if self.image.width > screen_width or self.image.height > screen_height:
            if aspect_ratio > 1:
                new_width = screen_width - 50
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = screen_height - 100
                new_width = int(new_height * aspect_ratio)

            self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(new_width, new_height)

        self.tk_image = ImageTk.PhotoImage(self.image)

        # Update the canvas dimensions
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image, tags="background")

        self.label.config(text="Click on the image to log coordinates")

        self.canvas.bind("<Button-1>", self.log_click_women)
        self.canvas.bind("<Button-3>", self.log_click_men)

    def log_click_women(self, event):
        x, y = event.x, event.y
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        with open(self.log_file_women, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x, y, timestamp])

        print(f"Logged (Women): X={x}, Y={y}, Time={timestamp}")

        # Redraw the original image to reset the canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image, tags="background")

        # Draw high heel images for all previous clicks
        for click in self.previous_clicks_women:
            self.canvas.create_image(click[0], click[1], image=self.tk_image_heel, anchor=tk.CENTER)

        # Draw sneaker images for all previous men's clicks
        for click in self.previous_clicks_men[:-1]:
            self.canvas.create_image(click[0], click[1], image=self.tk_image_sneaker, anchor=tk.CENTER)
        if self.previous_clicks_men:
            last_click = self.previous_clicks_men[-1]
            self.canvas.create_image(last_click[0], last_click[1], image=self.tk_image_man2, anchor=tk.CENTER)

        # Draw a woman image for the current click
        self.canvas.create_image(x, y, image=self.tk_image_woman, anchor=tk.CENTER)

        # Save the current click as the most recent
        self.previous_clicks_women.append((x, y))

    def log_click_men(self, event):
        x, y = event.x, event.y
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        with open(self.log_file_men, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x, y, timestamp])

        print(f"Logged (Men): X={x}, Y={y}, Time={timestamp}")

        # Redraw the original image to reset the canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image, tags="background")

        # Draw high heel images for all previous women's clicks
        for click in self.previous_clicks_women[:-1]:
            self.canvas.create_image(click[0], click[1], image=self.tk_image_heel, anchor=tk.CENTER)
        if self.previous_clicks_women:
            last_click = self.previous_clicks_women[-1]
            self.canvas.create_image(last_click[0], last_click[1], image=self.tk_image_woman2, anchor=tk.CENTER)

        # Draw sneaker images for all previous clicks
        for click in self.previous_clicks_men:
            self.canvas.create_image(click[0], click[1], image=self.tk_image_sneaker, anchor=tk.CENTER)

        # Draw a man image for the current click
        self.canvas.create_image(x, y, image=self.tk_image_man, anchor=tk.CENTER)

        # Save the current click as the most recent
        self.previous_clicks_men.append((x, y))

    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.save_folder = folder_path
            print(f"Selected folder: {self.save_folder}")

    def save_canvas(self, event=None):
        if not self.save_folder:
            print("No folder selected. Please click 'Select Folder' to choose a folder to save the image.")
            return

        file_name = time.strftime("canvas_%Y%m%d_%H%M%S.png")
        file_path = os.path.join(self.save_folder, file_name)

        try:
            # Capture the canvas content with higher DPI using the tkinter .postscript method
            self.canvas.update()
            ps_image_path = "temp_canvas.eps"
            self.canvas.postscript(file=ps_image_path, colormode='color', height=self.canvas.winfo_height(), width=self.canvas.winfo_width(), pagewidth=self.canvas.winfo_width() * 3.0, pageheight=self.canvas.winfo_height() * 3.0)

            # Convert the PostScript file to an image using Pillow
            img = Image.open(ps_image_path)
            img.load(scale=4)  # Scale the image for higher resolution
            img.save(file_path, "PNG")

            print(f"Canvas saved as {file_path}")

        except Exception as e:
            print(f"Error saving canvas: {e}")

        finally:
            # Ensure temporary files are cleaned up
            if os.path.exists(ps_image_path):
                try:
                    os.remove(ps_image_path)
                except Exception as cleanup_error:
                    print(f"Error cleaning up temporary files: {cleanup_error}")

    

    # def save_canvas(self, event=None):
    #     if not self.save_folder:
    #         print("No folder selected. Please click 'Select Folder' to choose a folder to save the image.")
    #         return
    
    #     file_name = time.strftime("canvas_%Y%m%d_%H%M%S.png")
    #     file_path = os.path.join(self.save_folder, file_name)
    
    #     try:
    #         # Get the absolute screen coordinates of the canvas
    #         x = self.canvas.winfo_rootx()
    #         y = self.canvas.winfo_rooty()
    #         x1 = x + self.canvas.winfo_width()
    #         y1 = y + self.canvas.winfo_height()
    
    #         # Capture the canvas content
    #         img = ImageGrab.grab(bbox=(x, y, x1, y1))
    #         img.save(file_path, "PNG")
    
    #         print(f"Canvas saved as {file_path}")
    
    #     except Exception as e:
    #         print(f"Error saving canvas: {e}")






if __name__ == "__main__":
    root = tk.Tk()
    app = ImageClickApp(root)
    root.mainloop()

