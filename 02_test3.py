# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 09:39:39 2023

@author: guill
"""

import whdynamic as wh
import numpy as np
import cv2
import time
from src import CameraWatcher
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# =============================================================================
# # FUNCTIONS
# =============================================================================

def take_image():
    # take image
    img_buffer = cams.get_image(0)
    # load the image
    Jpeg_file = Image.open(img_buffer)
    # convert image to numpy array and compute average
    data = np.asarray(Jpeg_file)
    image = (data[:,:,0] + data[:,:,1] + data[:,:,2]) // 3
    
    return image


# =============================================================================
# # INPUTS
# =============================================================================

''' RECORDA QUE TENS deg AL NOM D'ARXIU '''

order = 7 # resolution = 2 ** (order - 1)
save_file = True
fps_in = 5 # camera handles around 6.5 fps max
delay = 0
degrees = 10 # Real life cam-projector displacement
# shown_fraction = 1 # Still not implemented with dynamic wh creation

# =============================================================================
# # STARTUP
# =============================================================================

if not save_file:
    order = 3 # tests only

# DEFINE PARAMETERS
W = wh.W(order) # Matrix for the hadamard_ij() function
res = 2 ** (order - 1) # resolution

print('Expected runtime =', "{:.2f}".format((1.8 * 2/fps_in * res ** 2) / 60), 'minutes')
hs = res # hadamard size
mw = hs * 16 // 9 # matrix width (squares to fill the screen)
matrix_i = np.uint8(np.zeros((hs, mw))) # generate matrix to be shown

# START FULLSCREEN WINDOW
cv2.namedWindow('crame',cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('crame',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
if save_file:
    cv2.waitKey(15000)

# START CAMERA
cams = CameraWatcher(1)
cams.watch_camera(("192.168.1.83", 8000), shutter_speed=300000)

# GET CAMERA IMAGE INFO
data = take_image()
h, w = data.shape

# TEST FIRST 17 IMAGES
Images_0 = np.empty([h, w, 17], dtype=np.uint8()) 
Images_1 = np.empty([h, w, 17], dtype=np.uint8()) 

# =============================================================================
# # DATA GETHERING
# =============================================================================

reconstruction = np.zeros((res, res), dtype=np.float64())

t_ini = time.time()
c = 0

for invert in [False, True]:
    for i in range(res):
        for j in range(res):
            
            # Create matrix
            wh_matrix = 255 * wh.hadamard_ij(W, i, j, invert)
            
            # Fill central square and project matrix
            matrix_i[:,(mw - hs) // 2 : (mw + hs) // 2] = wh_matrix
            cv2.imshow('crame', matrix_i)
            
            # Important pause before taking the image
            cv2.waitKey(1000//fps_in)
            
            # TAKE IMAGE
            image = take_image()
            
            if c<17:
                # Save first 17 images for debugging
                Images_0[:,:,c] = image
                c+=1
            
            # Calculate intensity
            intensity = image[:,(w-h)//2:(w-h)//2+h].mean()
            
            # Account for the delay of the captures
            ii, jj = i, (j - delay) % res
            if (j - delay) < 0:
                ii -= 1
            ii, jj = (ii < 0) * 0 + (ii >= 0) * ii, (ii < 0) * 0 + (ii >= 0) * jj
             
            # Add to the reconstructed image
            reconstruction += intensity * wh.hadamard_ij(W, ii, jj, invert)
            

# Close camera
cams.close()

# Time metrics
t_fin = time.time()
t_tot = t_fin - t_ini
fps = 2 * res ** 2 / t_tot

# save file
if save_file:
    
    filename = str('reconstructions/' + str(int(time.time())) + '_x' 
                   + str(res) + '_fps' + str(int(fps_in)) + '_del'
                   + str(delay) + '_deg' + str(degrees))
    np.save(filename, reconstruction)



# =============================================================================
# # PLOTS & OUTPUT
# =============================================================================

print("{:.2f}".format(fps_in), 'fps in')
print("{:.2f}".format(fps), 'fps out')
print("Runtime = ", "{:.2f}".format(t_tot))

# Show reconstruction
plt.figure()
plt.imshow(reconstruction, cmap='gray')
plt.axis('off')

# Show first 17 images
plt.figure()
for n in range(16):
    
    plt.subplot(int(np.sqrt(2 * 17) + 1), int(np.sqrt(2 * 17) + 1), 2 * n + 1)
    plt.imshow(Images_0[:,:,n], cmap='gray')
    plt.axis('off')
    
    ''' ARREGLAR PLOT '''
    plt.subplot(int(np.sqrt(2 * 17) + 1), int(np.sqrt(2 * 17) + 1), 2 * n + 2)
    plt.imshow(wh.hadamard_ij(W, n // 4, n % 4, invert=False)  , cmap='gray')
    plt.axis('off') 
    
    plt.tight_layout()

