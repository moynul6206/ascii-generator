from tkinter import Tk, Label, Button, filedialog, Text
from PIL import Image
import pyperclip

# ASCII characters used for different brightness levels
ascii_chars = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# Function to convert RGB to grayscale
def rgb_to_gray(r, g, b):
    return 0.2989 * r + 0.5870 * g + 0.1140 * b

# Function to convert grayscale to ASCII characters
def grayscale_to_ascii(gray_value):
    char_index = int(gray_value / 25.6)  # Adjust this value for better results
    return ascii_chars[char_index]

# Function to resize image
def resize_image(image, new_width=100):
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    return resized_image

# Function to convert image to ASCII art
def image_to_ascii(image):
    image = resize_image(image)
    image = image.convert('RGB')
    ascii_art = ''
    for y in range(image.height):
        for x in range(image.width):
            (r, g, b) = image.getpixel((x, y))
            gray_value = rgb_to_gray(r, g, b)
            ascii_char = grayscale_to_ascii(gray_value)
            ascii_art += ascii_char
        ascii_art += '\n'
    return ascii_art

# Function to handle file upload button
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', ['.png', '.jpg', '.jpeg', '.gif'])])
    if file_path:
        image = Image.open(file_path)
        ascii_art = image_to_ascii(image)
        copy_ascii_button.config(state='normal')
        save_ascii_button.config(state='normal')
        ascii_text.config(state='normal')
        ascii_text.delete('1.0', 'end')
        ascii_text.insert('1.0', ascii_art)
        ascii_text.config(state='disabled')

# Function to handle copy ASCII art button
def copy_ascii():
    ascii_art = ascii_text.get('1.0', 'end-1c')
    pyperclip.copy(ascii_art)

# Function to handle save ASCII art button
def save_ascii():
    ascii_art = ascii_text.get('1.0', 'end-1c')
    file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', ['.txt'])])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(ascii_art)

# Create the main window
window = Tk()
window.title("ASCII Art Generator")

# Create labels and buttons
upload_label = Label(window, text="Upload an image:")
upload_label.pack()
upload_button = Button(window, text="Upload", command=upload_file)
upload_button.pack()

ascii_text = Text(window, height=20, width=60, state='disabled')
ascii_text.pack()

copy_ascii_button = Button(window, text="Copy ASCII Art", command=copy_ascii, state='disabled')
copy_ascii_button.pack()

save_ascii_button = Button(window, text="Save as Text", command=save_ascii, state='disabled')
save_ascii_button.pack()

# Run the main window
window.mainloop()
