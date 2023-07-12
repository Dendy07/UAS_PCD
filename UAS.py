import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg


def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image = Image.open(file_path)
        original_image = image.copy()
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)

        rgb_canvas.image = photo
        rgb_canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        # Store the original image
        root.original_image = original_image


def convert_to_grayscale():
    original_image = root.original_image
    if original_image:
        grayscale_image = original_image.convert("L")
        grayscale_image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(grayscale_image)

        grayscale_canvas.image = photo
        grayscale_canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        # Update the stored grayscale image
        root.grayscale_image = grayscale_image

def update_histogram():
    grayscale_image = root.grayscale_image
    if grayscale_image:
        histogram = grayscale_image.histogram()

        plt.figure()
        plt.title('Histogram')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.hist(histogram, bins=256, color='gray')

        # Calculate brightness from histogram
        total_pixels = grayscale_image.width * grayscale_image.height
        brightness = sum(histogram[128:]) / total_pixels
        brightness_text = "Terang" if brightness > 0.5 else "Gelap"

        # Add text label for brightness
        plt.text(0.8, 0.9, brightness_text, transform=plt.gca().transAxes, color='red')

        # Update the histogram figure
        histogram_canvas.figure = plt.gcf()
        histogram_canvas.draw()

def calculate_mse_psnr():
    original_image = root.original_image
    grayscale_image = root.grayscale_image
    if original_image and grayscale_image:
        original_np = np.array(original_image.resize((grayscale_image.width, grayscale_image.height)))
        grayscale_np = np.array(grayscale_image)
        
        # Check if grayscale_np has 3 channels (expand dimensions if needed)
        if len(grayscale_np.shape) == 2:
            grayscale_np = np.expand_dims(grayscale_np, axis=2)

        mse = np.mean(np.square(original_np - grayscale_np))
        psnr = 10 * np.log10((255 ** 2) / mse)
        mse_label.config(text=f"MSE: {mse:.2f}")
        psnr_label.config(text=f"PSNR: {psnr:.2f} dB")


# Create the main window
root = tk.Tk()
root.title("Image Processing")

# Create Open Image button
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(pady=10)

# Create a frame for RGB and Grayscale
frame_rgb = tk.Frame(root)
frame_rgb.pack(side=tk.LEFT, padx=10, pady=10)

frame_grayscale = tk.Frame(root)
frame_grayscale.pack(side=tk.LEFT, padx=10, pady=10)

# Create a canvas to display the RGB image
rgb_canvas = tk.Canvas(frame_rgb, width=400, height=400)
rgb_canvas.pack()

# Create a canvas to display the grayscale image
grayscale_canvas = tk.Canvas(frame_grayscale, width=400, height=400)
grayscale_canvas.pack()

# Create Convert to Grayscale button
grayscale_button = tk.Button(root, text="Convert to Grayscale", command=convert_to_grayscale)
grayscale_button.pack(pady=10)

# Create Histogram button
histogram_button = tk.Button(root, text="Histogram", command=update_histogram)
histogram_button.pack(pady=10)

# Create a frame for the histogram and metrics
histogram_frame = tk.Frame(root)
histogram_frame.pack(pady=10)

# Create a Figure and Axes for the histogram
histogram_figure = plt.figure()
histogram_axes = histogram_figure.add_subplot(111)

# Create a FigureCanvasTkAgg to display the histogram
histogram_canvas = tkagg.FigureCanvasTkAgg(histogram_figure, master=histogram_frame)
histogram_canvas.draw()
histogram_canvas.get_tk_widget().pack(side=tk.TOP)

# Create a frame for the metrics
metrics_frame = tk.Frame(root)
metrics_frame.pack(pady=10)

# Create MSE and PSNR labels
mse_label = tk.Label(metrics_frame, text="MSE: ")
mse_label.pack(side=tk.LEFT, padx=5)

psnr_label = tk.Label(metrics_frame, text="PSNR: ")
psnr_label.pack(side=tk.LEFT, padx=5)

# Create Calculate button
calculate_button = tk.Button(root, text="Calculate MSE and PSNR", command=calculate_mse_psnr)
calculate_button.pack(pady=10)

# Initialize variables
root.original_image = None
root.grayscale_image = None

# Start the main loop
root.mainloop()
