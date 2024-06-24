from PIL import Image, ImageTk
import binascii
import io
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import zlib

def encode_image_to_unagi(input_image_path, output_file_path):
    try:
        with Image.open(input_image_path) as img:
            raw_data = img.tobytes()
            mode = img.mode
            size = img.size
            
            hex_data = binascii.hexlify(raw_data).decode('utf-8')
            
            compressed_hex_data = zlib.compress(hex_data.encode('utf-8'))
            
            with open(output_file_path, 'wb') as file:
                file.write(f"{mode}\n".encode('utf-8'))
                file.write(f"{size[0]} {size[1]}\n".encode('utf-8'))
                file.write(compressed_hex_data)
                
        print(f"Image encoded to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while encoding the image: {e}")

def decode_unagi_to_image(input_file_path):
    try:
        with open(input_file_path, 'rb') as file:
            mode = file.readline().strip().decode('utf-8')
            size = tuple(map(int, file.readline().strip().split()))
            compressed_hex_data = file.read()
            
        hex_data = zlib.decompress(compressed_hex_data).decode('utf-8')
        
        raw_data = binascii.unhexlify(hex_data.encode('utf-8'))
        
        img = Image.frombytes(mode, size, raw_data)
        
        return img
    except Exception as e:
        print(f"An error occurred while decoding the image: {e}")
        return None

def open_image(filepath):
    img = decode_unagi_to_image(filepath)
    if img:
        img.thumbnail((800, 800))
        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk
        root.title(f"Unagi Image Viewer - {filepath}")
    else:
        messagebox.showerror("Error", "Failed to load the image.")

def show_help():
    help_text = """
    Usage:
        unagi.py <command> <input_path> <output_path>
    
    Commands:
        encode  <input_image_path> <output_unagi_path>    Encode an image to .unagi format
        decode  <input_unagi_path> <output_image_path>    Decode a .unagi file to an image
        view    <input_unagi_path>                        View a .unagi file in the viewer
    """
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_path = sys.argv[1]
        root = tk.Tk()
        root.title("Unagi Image Viewer")

        label = tk.Label(root)
        label.pack()

        open_image(input_path)

        root.mainloop()
    elif len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        show_help()
    else:
        action = sys.argv[1]

        if action == "encode" and len(sys.argv) == 4:
            input_path = sys.argv[2]
            output_path = sys.argv[3]
            encode_image_to_unagi(input_path, output_path)
        elif action == "decode" and len(sys.argv) == 4:
            input_path = sys.argv[2]
            output_path = sys.argv[3]
            img = decode_unagi_to_image(input_path)
            if img:
                img.save(output_path)
        elif action == "view" and len(sys.argv) == 3:
            input_path = sys.argv[2]
            root = tk.Tk()
            root.title("Unagi Image Viewer")

            label = tk.Label(root)
            label.pack()

            open_image(input_path)

            root.mainloop()
        else:
            show_help()
