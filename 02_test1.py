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
from PIL import Image
import matplotlib.pyplot as plt
import random



# =============================================================================
# # INPUTS
# =============================================================================

''' RECORDA QUE TENS deg AL NOM D'ARXIU '''

save_file = True
fps_in = 11 # camera handles around 6.5 fps max
delay = 1
shown_fraction = 1

# =============================================================================
# # STARTUP
# =============================================================================

# LOAD HADAMARD ARRAYS
hadamard_basis_0 = np.load('hadamard/wh0_0_64.npy')
hadamard_basis_1 = np.load('hadamard/wh1_1_64.npy')

if np.max(hadamard_basis_0) == 1:
    hadamard_basis_0 = 180 * hadamard_basis_0
    hadamard_basis_1 = 180 * hadamard_basis_1

if np.min(hadamard_basis_0) != 0:
    hadamard_basis_0 -= np.min(hadamard_basis_0)
    hadamard_basis_1 -= np.min(hadamard_basis_1)

# DEFINE PARAMETERS
hs = hadamard_basis_0.shape[0] # hadamard size
mw = hs * 16 // 9 # matrix width (squares to fill the screen)
matrix_i = np.uint8(np.zeros((hs, mw))) # generate matrix to be shown
N = hadamard_basis_0.shape[2] # number of hadamard matrices
if not save_file:
    N = 17 # tests only
    shown_fraction = 1 # tests only
print('Expected runtime =', "{:.2f}".format((2.5 * 2/fps_in * shown_fraction * N)))

# HADAMARD SAMPLE TO BE USED
shown0 = sorted(random.sample(range(N), int(N * shown_fraction))) 
shown1 = sorted(random.sample(range(N), int(N * shown_fraction)))

# START FULLSCREEN WINDOW
cv2.namedWindow('crame',cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('crame',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
if save_file:
    cv2.waitKey(15000)

# START CAMERA
cams = CameraWatcher(1)
cams.watch_camera(("192.168.1.83", 8000), shutter_speed=300000)

# GET CAMERA IMAGE INFO
# take image
img_buffer = cams.get_image(0)
# load the image
Jpeg_file = Image.open(img_buffer)
# convert image to numpy array
data = np.asarray(Jpeg_file)
# Store first ones for tests
h, w = data.shape[:2]
Images_0 = np.empty([h, w, 17], dtype=np.uint8()) 
Images_1 = np.empty([h, w, 17], dtype=np.uint8()) 

Intensities = np.zeros([N,2])


# =============================================================================
# # DATA GETHERING
# =============================================================================

t_ini = time.time()
c = 0
for i in shown0:
    
    # fill central square and project matrix
    matrix_i[:,(mw - hs) // 2 : (mw + hs) // 2] = hadamard_basis_0[:,:,i] 
    cv2.imshow('crame', matrix_i)
    
    # PAUSA MOLT IMPORTANT ABANS DE PRENDRE IMATGE
    cv2.waitKey(1000//fps_in)
    
    # take image
    img_buffer = cams.get_image(0)
    # load the image
    Jpeg_file = Image.open(img_buffer)
    # convert image to numpy array and compute average
    data = np.asarray(Jpeg_file)
    image = (data[:,:,0] + data[:,:,1] + data[:,:,2]) // 3    
    
    if c<17:
        # Save image
        Images_0[:,:,c] = image
        c+=1
        
    Intensities[i,0] = image[:,(w-h)//2:(w-h)//2+h].mean()

c = 0
for i in shown1:
    
    # fill central square and project matrix
    matrix_i[:,(mw - hs) // 2 : (mw + hs) // 2] = hadamard_basis_1[:,:,i] 
    cv2.imshow('crame', matrix_i)    
    
    # FPS (IMPORTANT TO CHECK SYNCHRONISATION)
    cv2.waitKey(1000//fps_in)
    
    # take image
    img_buffer = cams.get_image(0)
    # load the image
    Jpeg_file = Image.open(img_buffer)
    # convert image to numpy array and compute average
    data = np.asarray(Jpeg_file)
    image = (data[:,:,0] + data[:,:,1] + data[:,:,2]) // 3
    
    if c<17:
        # Save image
        Images_1[:,:,c] = image
        c+=1        

    Intensities[i,1] = image[:,(w-h)//2:(w-h)//2+h].mean() 

# Close camera
cams.close()

# Time metrics
t_fin = time.time()
t_tot = t_fin - t_ini
fps = 2 * len(shown0) / t_tot

# Reconstruction taking the delay into account
reconstruction = np.zeros(hadamard_basis_0.shape[:2])

for i in range(len(shown0)-delay):
    a, b = shown0[i+delay], shown0[i]
    reconstruction += Intensities[a,0] / Intensities.max() * hadamard_basis_0[:,:,b] / hadamard_basis_0.max()
    
for i in range(len(shown1)-delay):
    a, b = shown1[i+delay], shown1[i]
    reconstruction += Intensities[a,1] / Intensities.max() * hadamard_basis_1[:,:,b] / hadamard_basis_1.max()

reconstruction /= (2 * len(shown0))  # normalize

# save file
if save_file:
    
    filename = str('reconstructions/' + str(int(time.time())) + '_x' 
                   + str(int(np.sqrt(N))) + '_fps' + str(int(fps_in)) + '_d'
                   + str(delay) + '_p' + str(shown_fraction)+'deg10')
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

# Show first images
plt.figure()
for n in range(9):
    
    plt.subplot(int(np.sqrt(2 * 17) + 1), int(np.sqrt(2 * 17) + 1), 2 * n + 1)
    plt.imshow(Images_0[:,:,n], cmap='gray')
    # plt.title("{:.2f}".format(Images_0[:,:,n].mean()))
    plt.axis('off')
    
    a = shown0[n]
    plt.subplot(int(np.sqrt(2 * 17) + 1), int(np.sqrt(2 * 17) + 1), 2 * n + 2)
    plt.imshow(hadamard_basis_0[:,:,a], cmap='gray')
    # plt.imshow(Images_1[:,:,a], cmap='gray')
    # plt.title("{:.2f}".format(Images_1[:,:,a].mean()))
    plt.axis('off') 
    
    plt.tight_layout()

