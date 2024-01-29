# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:03:02 2023

@author: guill
"""

import os
from PIL import Image
import numpy as np

directory = "C:/Users/guill/Desktop/UNI/Grau Física/8è semestre/TFG/netcam-main/netcam-main/reconstructions/cable tests" # replace with the path to your directory

# Get all the files in the directory
files = os.listdir(directory)

# Loop through each file
for file in files:
    # Check if the file has the ".npy" extension
    if file.endswith(".npy"):
        # Load the numpy array from the file
        arr = np.load(os.path.join(directory, file))

        # Convert the numpy array to an unsigned integer data type
        arr = (arr - arr.min()) * (255 / (arr.max() - arr.min()))
        arr = np.uint8(arr)
        if arr.shape[0] > 64 or arr.shape[1] > 64:
            # Get the center of the image
            arr = arr[:,(np.abs(arr.shape[0]-arr.shape[1])//2):((arr.shape[0]+arr.shape[1])//2)]
                
        # Convert the numpy array to a PIL Image
        img = Image.fromarray(arr)
               
        # Get the new filename with ".jpg" extension
        new_filename = os.path.splitext(file)[0] + ".jpg"

        # Save the PIL Image with the new filename
        img.save(os.path.join(directory, new_filename))
        

for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        filepath = os.path.join(directory, filename)

        # open the image and check if it's larger than 64x64
        with Image.open(filepath) as img:
            if img.size[0] > 64 or img.size[1] > 64:
                # downscale the image to 64x64
                img.thumbnail((64, 64), Image.ANTIALIAS)
                # save the downcaled image with "downscaled" prefix
                downscale_filepath = os.path.join(directory, "downscaled_" + filename)
                img.save(downscale_filepath)

                print(f"{filename} was downscaled and saved as {os.path.basename(downscale_filepath)}")
            else:
                print(f"{filename} is already smaller than 64x64 and was not downscaled.")






# =============================================================================
# 
# for filename in os.listdir(directory):
#     if filename.endswith('.jpg'):
#         filepath = os.path.join(directory, filename)
#         with Image.open(filepath) as img:
#             if img.size[0] < 128 or img.size[1] < 128:
#                 img = img.resize((512, 512), resample=Image.BICUBIC)
#                 img.save(filepath)
# =============================================================================
# =============================================================================
# 
# import os
# from PIL import Image
# import numpy as np
# 
# # Set the directory path
# directory = "C:/Users/guill/Desktop/UNI/Grau Física/8è semestre/TFG/netcam-main/netcam-main/reconstructions"
# 
# # Get all the files in the directory
# files = os.listdir(directory)
# 
# # Loop through each file
# for file in files:
#     # Check if the file has the ".npy" extension
#     if file.endswith(".npy"):
#         # Load the numpy array from the file
#         arr = np.load(os.path.join(directory, file))
# 
#         # Convert the numpy array to an unsigned integer data type
#         arr = (arr - arr.min()) * (255 / (arr.max() - arr.min()))
#         arr = np.uint8(arr)
# 
#         # Convert the numpy array to a PIL Image
#         img = Image.fromarray(arr)
# 
#         # Get the new filename with ".jpg" extension
#         new_filename = os.path.splitext(file)[0] + ".jpg"
# 
#         # Save the PIL Image with the new filename
#         img.save(os.path.join(directory, new_filename))
# 
# =============================================================================
# =============================================================================
# import os
# import numpy as np
# 
# mainpath = str('C:/Users/guill/Desktop/UNI/Grau Física/8è semestre/TFG/netcam-main/netcam-main/reconstructions')
# 
# files = os.listdir(mainpath)
# 
# 
# for file in files:
#     path = 'reconstructions/' + str(file)
#     im = np.load(path)
# 
# 
# # im = np.load('hadamard/wh1_1_128.npy')
# 
# print('MAX:  ',im.max(),'\nMIN:  ', im.min(),'\nMean: ', im.mean(),
#       '\nRange:', im.max() - im.min())
# 
# 
# =============================================================================
