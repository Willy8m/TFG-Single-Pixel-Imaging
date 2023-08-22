# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:54:55 2023

@author: guill
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

res=6
delay=1
a1 = np.empty((res,res,2))
for i in range(res):
    for j in range(res):
        
        ii = i
        if (j - delay) < 0:
            ii -= 1
        jj = (j - delay) % res
        ii, jj = (ii < 0) * 0 + (ii >= 0) * ii, (ii < 0) * 0 + (ii >= 0) * jj
        
        a1[i,j,0] = str(i) + str(j)
        a1[i,j,1] = str(ii) + str(jj)
        
        
a1[:,:,0], a1[:,:,1]





# =============================================================================
# hadamard_basis = np.load('hadamard/wh1_8.npy')
# hadamard_basis_1 = np.load('hadamard/wh1_1_8.npy')
# N = hadamard_basis.shape[2]
# 
# plt.figure()
# 
# for n in range(N):
#     plt.subplot(int(np.sqrt(2 * N) + 1), int(np.sqrt(2 * N) + 1), 2 * n + 1)
#     plt.imshow(hadamard_basis[:,:,n])
#     plt.axis('off')
#     plt.subplot(int(np.sqrt(2 * N) + 1), int(np.sqrt(2 * N) + 1), 2 * n + 2)
#     plt.imshow(hadamard_basis_1[:,:,n])
#     plt.axis('off')    
#     
# =============================================================================

# =============================================================================
# b = np.array([[[1,2],[3,4]],[[1,2],[3,4]]])
# d = 2 * b
# a = np.append(b,d, axis=0) 
# 
# for i in range(0,25):
#     a = np.append(a, d*i, axis = 0)
# =============================================================================
    
# SCREEN SIZE (MONITORS 1 & 2)
# =============================================================================
# import ctypes
# import screeninfo
# user32 = ctypes.windll.user32
# screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# total_screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
# =============================================================================

# =============================================================================
# 
# 
# if __name__ == '__main__':
#     screen_id = 0
#     is_color = False
# 
#     # get the size of the screen
#     screen = screeninfo.get_monitors()[screen_id]
#     width, height = screen.width, screen.height
# 
#     # create image
#     if True:
#         image = np.ones((height, width, 3), dtype=np.float32)
#         image[:10, :10] = 0  # black at top-left corner
#         image[height - 10:, :10] = [1, 0, 0]  # blue at bottom-left
#         image[:10, width - 10:] = [0, 1, 0]  # green at top-right
#         image[height - 10:, width - 10:] = [0, 0, 1]  # red at bottom-right
#     else:
#         image = np.ones((height, width), dtype=np.float32)
#         image[0, 0] = 0  # top-left corner
#         image[height - 2, 0] = 0  # bottom-left
#         image[0, width - 2] = 0  # top-right
#         image[height - 2, width - 2] = 0  # bottom-right
# 
#     window_name = 'projector'
#     cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
#     cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
#     cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
#                           cv2.WINDOW_FULLSCREEN)
#     cv2.imshow(window_name, image)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
# =============================================================================
