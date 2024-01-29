# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:33:40 2023

@author: guill
"""

import numpy as np
from scipy import fftpack, ndimage
import matplotlib.pyplot as plt
from PIL import Image
import os

# Load the JPEG image
im = np.array(Image.open('reconstructions/x64_fps30_deg80turbulent.jpg'))

# Convert to grayscale if needed
if len(im.shape) == 3 and im.shape[2] == 3:
    im = np.dot(im[...,:3], [0.2989, 0.5870, 0.1140])

# Compute the 2D FFT of the image
im_fft = fftpack.fftshift(fftpack.fft2(im))

# High-pass filter
cutoff = 23
rows, cols = im_fft.shape
crow, ccol = rows//2, cols//2
mask = np.zeros((rows, cols))
mask[crow-cutoff:crow+cutoff, ccol-cutoff:ccol+cutoff] = 1
im_fft_filt = im_fft * mask

# Compute the inverse 2D FFT of the filtered image
im_filt = np.real(fftpack.ifft2(fftpack.fftshift(im_fft_filt)))

# Display the original and filtered images
plt.subplot(2, 2, 1)
plt.imshow(im, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(im_filt, cmap='gray')
plt.title('Filtered Image')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(np.abs(im_fft), cmap='gray')
plt.title('Filtered Image')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(np.abs(im_fft_filt), cmap='gray')
plt.title('Filtered Image')
plt.axis('off')

plt.show()


np.save