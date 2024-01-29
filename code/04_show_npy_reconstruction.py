# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:03:02 2023

@author: guill
"""

import numpy as np
import matplotlib.pyplot as plt

im = np.load('reconstructions/1677068633_x64_fps11_d1_p1.npy')

# im = np.load('hadamard/wh1_1_128.npy')

print('MAX:  ',im.max(),'\nMIN:  ', im.min(),'\nMean: ', im.mean(),
      '\nRange:', im.max() - im.min())

plt.figure()

plt.imshow(im[:,:], cmap='gray')
