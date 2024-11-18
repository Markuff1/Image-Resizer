import cv2
from tkinter import Tk, Label, Button, Entry, filedialog, IntVar, messagebox

def compress_image(input_path, output_path, quality=85, max_size=(1920, 1080)):
    """
    Compress an image using OpenCV by resizing and adjusting JPEG quality.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the compressed image.
        quality (int): JPEG compression quality (1-100). Lower values result in smaller files.
        max_size (tuple): Maximum dimensions (width, height) for resizing.
    """
    try:
        # Read the image using OpenCV
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError("Could not read the input image file.")
        
        # Get original dimensions
        original_height, original_width = img.shape[:2]
        
        # Calculate resizing scale
        scale_width = max_size[0] / original_width
        scale_height = max_size[1] / original_height
        scale = min(scale_width, scale_height, 1)  # Ensure we don't upscale the image
        
        # Resize the image if necessary
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Save the compressed image
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        success = cv2.imwrite(output_path, resized_img, encode_param)
        
        if not success:
            raise ValueError("Failed to write the output image file.")
        
        messagebox.showinfo("Success", f"Image compressed and saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compress image: {e}")

def select_input_file():
    """Open a file dialog to select the input image."""
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    input_path_entry.delete(0, 'end')  # Clear existing text
    input_path_entry.insert(0, file_path)

def select_output_file():
    """Open a file dialog to select the output image location."""
    file_path = filedialog.asksaveasfilename(
        title="Save Compressed Image As",
        defaultextension=".jpg",
        filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png"), ("All Files", "*.*")]
    )
    output_path_entry.delete(0, 'end')  # Clear existing text
    output_path_entry.insert(0, file_path)

def compress_image_from_ui():
    """Get inputs from the UI and compress the image."""
    input_path = input_path_entry.get()
    output_path = output_path_entry.get()
    quality = quality_var.get()
    max_width = max_width_var.get()
    max_height = max_height_var.get()

    if not input_path or not output_path:
        messagebox.showerror("Error", "Please select both input and output file paths.")
        return

    try:
        compress_image(input_path, output_path, quality=quality, max_size=(max_width, max_height))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Initialize the main window
root = Tk()
root.title("Image Compressor")
root.geometry("500x300")
root.resizable(False, False)

# Input file section
Label(root, text="Select Input Image:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
input_path_entry = Entry(root, width=40)
input_path_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

# Output file section
Label(root, text="Select Output Location:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_path_entry = Entry(root, width=40)
output_path_entry.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_output_file).grid(row=1, column=2, padx=10, pady=10)

# Quality section
Label(root, text="Compression Quality (1-100):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
quality_var = IntVar(value=85)  # Default quality
Entry(root, textvariable=quality_var, width=10).grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Maximum dimensions section
Label(root, text="Max Width:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
max_width_var = IntVar(value=1920)  # Default max width
Entry(root, textvariable=max_width_var, width=10).grid(row=3, column=1, padx=10, pady=10, sticky="w")

Label(root, text="Max Height:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
max_height_var = IntVar(value=1080)  # Default max height
Entry(root, textvariable=max_height_var, width=10).grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Compress button
Button(root, text="Compress Image", command=compress_image_from_ui, bg="green", fg="white").grid(
    row=5, column=0, columnspan=3, pady=20
)

# Run the main loop
root.mainloop()
