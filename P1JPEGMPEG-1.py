#!/usr/bin/env python
# coding: utf-8

# 1) Start a script called rgb_yuv.py and create a
# translator from 3 values in RGB into the 3 YUV
# values, plus the opposite operation

# In[6]:


def rgb_to_yuv(r, g, b):
    # Conversion from RGB to YUV
    y = 0.257 * r + 0.504 * g + 0.098 * b + 16
    u = -0.148 * r - 0.291 * g + 0.439 * b + 128
    v = 0.439 * r - 0.368 * g - 0.071 * b + 128
    return y, u, v

def yuv_to_rgb(y, u, v):
    # Conversion from YUV to RGB
    r = 1.164*(y - 16) + 1.596*(v - 128)
    g = 1.164*(y - 16) - 0.813*(v - 128) - 0.391*(u - 128)
    b = 1.164*(y - 16) + 2.018*(u - 128)
    return r, g, b

# Input RGB values
r_in = 255
g_in = 0
b_in = 0

# Convert RGB to YUV
y, u, v = rgb_to_yuv(r_in, g_in, b_in)
print(f"RGB to YUV: R={r_in}, G={g_in}, B={b_in} => Y={y}, U={u}, V={v}")

# Input YUV values
y_in = 255
u_in = 128
v_in = 128

# Convert YUV to RGB
r, g, b = yuv_to_rgb(y_in, u_in, v_in)
print(f"YUV to RGB: Y={y_in}, U={u_in}, V={v_in} => R={r}, G={g}, B={b}")


# 2) Use ffmpeg to resize images into lower quality.
# Use any image you like

# In[7]:


# Import subprocess to use ffmpeg and display the image
import subprocess
from PIL import Image

# Declare the input path and the name of the output
input_path = '/Users/arnauadan/Desktop/baixa.png'
output_path = 'baixa_output320x240.png'

# Declare the comand ffmpeg to scale the image 320:240 and save it
comand = f'ffmpeg -i "{input_path}" -vf scale=320:240 "{output_path}"'

# Save the result of the comand
result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Display the original image
input_image = Image.open(input_path)
display(input_image)

# Display the result image
output_image = Image.open(output_path)
display(output_image)


# 3) Create a method called serpentine which should
# be able to read the bytes of a JPEG file in the
# serpentine way we saw. 

# In[8]:


def read_bytes_of_JPED_serpentine(input):
    # We ensure that we can read as jpeg_file
    try:
        # Open the jpeg_file
        with open(input, 'rb') as jpeg_file:
            # Read the file as a byte serie
            jpeg_bytes = jpeg_file.read()
            # Return the bytes 
            return jpeg_bytes
    # If we can't return the exception FileNotFoundError as None
    except FileNotFoundError:
        return None
    
# Example how it works declaring the input path
input_path_color = '/Users/arnauadan/Desktop/colors.jpeg'
# Call the function made
jpeg_bytes = read_bytes_of_JPED_serpentine(input_path_color)
# Print the serpentine bytes 
print(jpeg_bytes)


# The result of these function is the read image as a serie of a bytes, on for every pixel. Here we can see the serpentine of bytes corresponding to our image.

# 4) Use FFMPEG to transform the previous image
# into b/w. Do the hardest compression you can.

# In[9]:


# Input path
input_path_color = '/Users/arnauadan/Desktop/colors.jpeg'
# Output name
output_path_bw = 'color_outputbw.jpeg'
# Comand to use ffmpeg to transform the image into a grey gamma
comand_bw = f'ffmpeg -i "{input_path_color}" -vf "format=gray" "{output_path_bw}"'

# Execute the result 
result = subprocess.Popen(comand_bw, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Display the original image
input_image = Image.open(input_path_color)
display(input_image)

# Display the resulting image
output_image = Image.open(output_path_bw)
display(output_image)


# 5) Create a method which applies a run-lenght
# encoding from a series of bytes given.

# In[10]:


def run_length_encoding(byte_series):
    # Declare the econded bytes as a bytearray() class
    encoded_bytes = bytearray()
    # Take the first byte of the byte_series recived
    current_byte = byte_series[0]
    # Start our counter on 1
    count = 1

    # Iterate for every byte of the byte_series entering
    for byte in byte_series[1:]:
        # Add to counter if the byte is repeated
        if byte == current_byte:
            count += 1
        # If the byte is not repeated
        else:
            # Add the preivous byte to the encoded_bytes bytearray
            encoded_bytes.append(current_byte)
            # Add how many bytes repeated found
            encoded_bytes.append(count)
            # Change the byte 
            current_byte = byte
            # Restart the counter to one
            count = 1

    # Add to the bytearray the last position
    encoded_bytes.append(current_byte)
    encoded_bytes.append(count)
    
    # Return the result
    return encoded_bytes

# Print the result of enconding of the serpentine bytes of the previous exercice
print(run_length_encoding(jpeg_bytes))


# The result show us that encoded works counting the repeated bytes and adding to the byte array compressed the number of how many are repeated. 

# 6) Create a class which can convert, can decode
# (or both) an input using the DCT. Not necessary a
# JPG encoder or decoder. A class only about DCT is
# OK too

# In[11]:


# Import the needed libary to perform the dct
from scipy.fftpack import dct, idct

# Inicialize the class
class DCTConverter:

    # Declare a function of dct
    def encode(data, block_size = 8):
        # Empty array
        encoded_data = []
        # Iterate into the data
        for i in range(0, len(data), block_size):
            # Take 8 blocks of the frame
            block = data[i:i + block_size]
            # Encoding the block computing the dct
            dct_block = dct(block, type=2, norm='ortho')
            # Add to the encoded data array
            encoded_data.extend(dct_block)
        # Return encoded data
        return encoded_data

    # Declare a function of the decode
    def decode(encoded_data, block_size = 8):
        # Empty array
        decoded_data = []
        # Iterate into the encoded array
        for i in range(0, len(encoded_data), block_size):
            # Take again 9 blocks of the encoded array
            dct_block = encoded_data[i:i + block_size]
            # Decode the block computing the idct
            block = idct(dct_block)
            # Add to the decoded data array
            decoded_data.extend(block)
        # Return the decoded data
        return decoded_data


# In[17]:


# Import the numpy library needed to transform our image to numpy array
import numpy as np

# Input path
input_path_color = '/Users/arnauadan/Desktop/colors.jpeg'

# Open the class
DCTConverter_ = DCTConverter()
# Open the image and transform into a flatten array 
array_image = np.array(Image.open(input_path_color)).flatten()

# Call the encode function from the DCTConcert class
encoded_array = DCTConverter.encode(array_image)

# Call the dencode function from the DCTConcert class
dencoded_array = DCTConverter.decode(encoded_array)

# Print the results
print(array_image)
print(encoded_array)
print(dencoded_array)

