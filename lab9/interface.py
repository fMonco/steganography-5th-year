import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import zipfile
import os

# LSB Replacement
def lsb_replacement(image_path, message, output_path, rate=1):
    image = Image.open(image_path)
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    
    message_bits = ''.join(format(ord(char), '08b') for char in message)
    total_bits = len(message_bits)
    
    if total_bits > len(flat_pixels) * rate:
        raise ValueError("Message is too large to hide in this image with the given rate.")
    
    for i in range(0, total_bits, rate):
        pixel_index = i // rate
        bits_to_replace = message_bits[i:i + rate].ljust(rate, '0')
        flat_pixels[pixel_index] = (flat_pixels[pixel_index] & (255 - (2 ** rate - 1))) | int(bits_to_replace, 2)
    
    new_pixels = flat_pixels.reshape(pixels.shape)
    new_image = Image.fromarray(new_pixels)
    new_image.save(output_path)

def lsb_extraction(image_path, message_length, rate=1):
    image = Image.open(image_path)
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    
    message_bits = ''
    for i in range(0, message_length * 8, rate):
        pixel_index = i // rate
        bits = flat_pixels[pixel_index] & (2 ** rate - 1)
        message_bits += format(bits, '0' + str(rate) + 'b')
    
    message = ''
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        message += chr(int(byte, 2))
    
    return message

# LSB Matching
def lsb_matching(image_path, message, output_path, rate=1):
    image = Image.open(image_path)
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    
    message_bits = ''.join(format(ord(char), '08b') for char in message)
    total_bits = len(message_bits)
    
    if total_bits > len(flat_pixels) * rate:
        raise ValueError("Message is too large to hide in this image with the given rate.")
    
    for i in range(0, total_bits, rate):
        pixel_index = i // rate
        target_bits = message_bits[i:i + rate].ljust(rate, '0')
        current_bits = format(flat_pixels[pixel_index], '08b')[-rate:]
        
        if current_bits != target_bits:
            if current_bits < target_bits:
                flat_pixels[pixel_index] += 1
            else:
                flat_pixels[pixel_index] -= 1
    
    new_pixels = flat_pixels.reshape(pixels.shape)
    new_image = Image.fromarray(new_pixels)
    new_image.save(output_path)

def lsb_matching_extraction(image_path, message_length, rate=1):
    return lsb_extraction(image_path, message_length, rate)

# Hamming Code Embedding
def hamming_encode(data):
    def calc_parity(bits, positions):
        return sum([int(bits[i - 1]) for i in positions]) % 2
    
    encoded = []
    for byte in data:
        bits = format(byte, '08b')
        p1 = calc_parity(bits, [1, 2, 4])
        p2 = calc_parity(bits, [1, 3, 4])
        p3 = calc_parity(bits, [2, 3, 4])
        encoded_bits = f'{p1}{p2}{bits[0]}{p3}{bits[1:]}'
        encoded.append(int(encoded_bits, 2))
    
    return encoded

def hamming_embedding(image_path, message, output_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    
    message_bytes = [ord(char) for char in message]
    encoded_message = hamming_encode(message_bytes)
    
    if len(encoded_message) > len(flat_pixels):
        raise ValueError("Message is too large to hide in this image.")
    
    for i in range(len(encoded_message)):
        flat_pixels[i] = encoded_message[i]
    
    new_pixels = flat_pixels.reshape(pixels.shape)
    new_image = Image.fromarray(new_pixels)
    new_image.save(output_path)

def hamming_decode(encoded_message):
    decoded_message = ''
    for encoded_byte in encoded_message:
        bits = format(encoded_byte, '08b')
        data_bits = bits[2] + bits[4:]
        decoded_message += chr(int(data_bits, 2))
    return decoded_message

def hamming_extraction(image_path, message_length):
    image = Image.open(image_path)
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    
    encoded_message = []
    for i in range(message_length * 2):
        encoded_message.append(flat_pixels[i])
    
    decoded_message = hamming_decode(encoded_message)
    return decoded_message

# Compression measurement
def compress_and_measure(image_path):
    with zipfile.ZipFile('temp.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(image_path, os.path.basename(image_path))
    size = os.path.getsize('temp.zip')
    os.remove('temp.zip')
    return size

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        
        self.image_path = ''
        
        self.create_widgets()

    def create_widgets(self):
        # File selection
        self.select_image_btn = tk.Button(self.root, text="Select Image", command=self.select_image)
        self.select_image_btn.pack()

        self.image_label = tk.Label(self.root, text="No image selected")
        self.image_label.pack()

        # Message entry
        self.message_label = tk.Label(self.root, text="Message to hide:")
        self.message_label.pack()

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack()

        # Method selection
        self.method_label = tk.Label(self.root, text="Select Method:")
        self.method_label.pack()

        self.method_var = tk.StringVar(value="LSB-R")
        self.lsb_r_radio = tk.Radiobutton(self.root, text="LSB-R", variable=self.method_var, value="LSB-R")
        self.lsb_r_radio.pack(anchor=tk.W)

        self.lsb_m_radio = tk.Radiobutton(self.root, text="LSB-M", variable=self.method_var, value="LSB-M")
        self.lsb_m_radio.pack(anchor=tk.W)

        self.hamming_radio = tk.Radiobutton(self.root, text="Hamming", variable=self.method_var, value="Hamming")
        self.hamming_radio.pack(anchor=tk.W)

        # Rate entry
        self.rate_label = tk.Label(self.root, text="Embedding Rate:")
        self.rate_label.pack()

        self.rate_entry = tk.Entry(self.root, width=10)
        self.rate_entry.pack()
        self.rate_entry.insert(0, "1")

        # Buttons for embedding and extracting
        self.embed_btn = tk.Button(self.root, text="Embed Message", command=self.embed_message)
        self.embed_btn.pack()

        self.extract_btn = tk.Button(self.root, text="Extract Message", command=self.extract_message)
        self.extract_btn.pack()

        # Compression analysis button
        self.compress_btn = tk.Button(self.root, text="Analyze Compression", command=self.analyze_compression)
        self.compress_btn.pack()

        # Result display
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if self.image_path:
            self.image_label.config(text=self.image_path)

    def embed_message(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected")
            return

        message = self.message_entry.get()
        rate = int(self.rate_entry.get())
        method = self.method_var.get()
        
        output_path = f"output_{method.lower()}.bmp"
        
        try:
            if method == "LSB-R":
                lsb_replacement(self.image_path, message, output_path, rate)
            elif method == "LSB-M":
                lsb_matching(self.image_path, message, output_path, rate)
            elif method == "Hamming":
                hamming_embedding(self.image_path, message, output_path)
            messagebox.showinfo("Success", f"Message embedded successfully. Output saved as {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_message(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected")
            return

        message_length = len(self.message_entry.get())
        rate = int(self.rate_entry.get())
        method = self.method_var.get()
        
        try:
            if method == "LSB-R":
                extracted_message = lsb_extraction(self.image_path, message_length, rate)
            elif method == "LSB-M":
                extracted_message = lsb_matching_extraction(self.image_path, message_length, rate)
            elif method == "Hamming":
                extracted_message = hamming_extraction(self.image_path, message_length)
            self.result_label.config(text=f"Extracted message: {extracted_message}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def analyze_compression(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected")
            return

        message = self.message_entry.get()
        rate = int(self.rate_entry.get())

        output_paths = {
            "LSB-R": "output_lsb-r.bmp",
            "LSB-M": "output_lsb-m.bmp",
            "Hamming": "output_hamming.bmp"
        }

        original_size = os.path.getsize(self.image_path)
        compression_results = []

        for method, output_path in output_paths.items():
            try:
                # Re-embed the message to ensure the output files are fresh
                if method == "LSB-R":
                    lsb_replacement(self.image_path, message, output_path, rate)
                elif method == "LSB-M":
                    lsb_matching(self.image_path, message, output_path, rate)
                elif method == "Hamming":
                    hamming_embedding(self.image_path, message, output_path)
                
                compressed_size = compress_and_measure(output_path)
                compression_results.append(f"{method}: {compressed_size} bytes")
            except Exception as e:
                compression_results.append(f"{method}: Error compressing")

        result_text = f"Original size: {original_size} bytes\n" + "\n".join(compression_results)
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
