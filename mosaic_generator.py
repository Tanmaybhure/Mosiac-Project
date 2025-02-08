import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, Canvas, PhotoImage, Frame
from PIL import Image, ImageTk

def adjust_element_mean(element_img, target_mean_value):
    """
    Adjusts the mean brightness of an image to match a target mean value.
    """
    current_mean = np.mean(element_img)
    adjustment = target_mean_value - current_mean
    adjusted_img = np.clip(element_img + adjustment, 0, 255).astype(np.uint8)
    return adjusted_img

def create_mosaic(small_img, big_img):
    """
    Creates a mosaic where each tile of the small image is adjusted to match
    the brightness of the corresponding pixel in the big image.
    """
    small_h, small_w = small_img.shape
    big_h, big_w = big_img.shape
    
    mosaic = np.zeros((big_h * small_h, big_w * small_w), dtype=np.uint8)
    
    for i in range(big_h):
        for j in range(big_w):
            target_mean = big_img[i, j]
            adjusted_tile = adjust_element_mean(small_img, target_mean)
            mosaic[i * small_h:(i + 1) * small_h, j * small_w:(j + 1) * small_w] = adjusted_tile
    
    return mosaic

class MosaicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mosaic Generator")
        self.root.geometry("600x700")
        self.root.configure(bg="#2c3e50")
        
        self.small_img_path = None
        self.big_img_path = None
        
        # Frame for buttons
        self.frame = Frame(root, bg="#34495e", pady=10, padx=10)
        self.frame.pack(pady=20)
        
        # Upload buttons
        Button(self.frame, text="Upload Small Image", command=self.upload_small_img, bg="#1abc9c", fg="white", font=("Arial", 12), padx=10, pady=5).pack(pady=5)
        Button(self.frame, text="Upload Big Image", command=self.upload_big_img, bg="#e67e22", fg="white", font=("Arial", 12), padx=10, pady=5).pack(pady=5)
        Button(self.frame, text="Generate Mosaic", command=self.generate_mosaic, bg="#e74c3c", fg="white", font=("Arial", 12), padx=10, pady=5).pack(pady=5)
        
        # Canvas to display images
        self.canvas = Canvas(root, width=500, height=500, bg="#ecf0f1", highlightthickness=2, highlightbackground="#95a5a6")
        self.canvas.pack()

    def upload_small_img(self):
        self.small_img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.small_img_path:
            self.display_image(self.small_img_path)
    
    def upload_big_img(self):
        self.big_img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.big_img_path:
            self.display_image(self.big_img_path)
    
    def generate_mosaic(self):
        if not self.small_img_path or not self.big_img_path:
            print("Please upload both images.")
            return
        
        # Load and convert images to grayscale
        small_img = cv2.imread(self.small_img_path, cv2.IMREAD_GRAYSCALE)
        big_img = cv2.imread(self.big_img_path, cv2.IMREAD_GRAYSCALE)
        
        if small_img is None or big_img is None:
            print("Error loading images.")
            return
        
        mosaic = create_mosaic(small_img, big_img)
        
        # Save and display the result
        output_path = "mosaic_output.png"
        cv2.imwrite(output_path, mosaic)
        self.display_image(output_path)
    
    def display_image(self, img_path):
        img = Image.open(img_path)
        img.thumbnail((500, 500))
        img = ImageTk.PhotoImage(img)
        
        self.canvas.create_image(250, 250, image=img)
        self.canvas.image = img

if __name__ == "__main__":
    root = tk.Tk()
    app = MosaicApp(root)
    root.mainloop()
