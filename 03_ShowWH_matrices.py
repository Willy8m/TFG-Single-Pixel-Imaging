# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 09:28:38 2023

@author: guill
"""

import cv2
import numpy as np

# Load

hadamard_basis_0 = np.load('hadamard/wh0_0_32.npy')

if np.max(hadamard_basis_0) == 1:
    
    hadamard_basis_0 = 10 + (180 * hadamard_basis_0)

# Arrange data

hs = hadamard_basis_0.shape[0] # hadamard size
mw = hs * 16 // 9 # matrix width (squares to fill the screen)

matrix_i = np.uint8(np.ones((hs, mw)) * 10) # generate matrix to be shown

# Show on window

a = 3

if a == 0:
    
    cv2.namedWindow('singleWH',cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('singleWH',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    matrix_i[:,(mw - hs) // 2 : (mw + hs) // 2] = hadamard_basis_0[:,:,0] 
    
    cv2.imshow('singleWH', matrix_i)
    
elif a == 1:
    
    cv2.namedWindow('singleWH',cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('singleWH',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    c = 0
    
    while True:
        
        matrix_i[:,(mw - hs) // 2 : (mw + hs) // 2] = hadamard_basis_0[:,:,c] 
        
        cv2.imshow('singleWH', matrix_i)
        
        cv2.waitKey(1010//30)
        
        c += 1
          
        if cv2.waitKey(1) & 0xFF == ord('q'):
            
            break

elif a == 2:
    
    import pygame
    from pygame.locals import *
    
    pygame.init()
    
    WIDTH = 1920
    HEIGHT = 1080
    
    windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    
    img = pygame.image.load("test.jpeg")
    
    while True:
       
        events = pygame.event.get()
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                
                pygame.quit()
                sys.exit()
        
        windowSurface.blit(img, (0, 0)) #Replace (0, 0) with desired coordinates
        
        pygame.display.flip()

    
elif a == 3:
    
    import whdynamic as wh
    
    order = 11
    
    sqrtN = 2 ** (order - 1)
    
    W = wh.W(order)
    
    hs = sqrtN # hadamard size
    mw = hs * 16 // 9 # matrix width (squares to fill the screen)
    
    matrix_i = np.uint8(np.zeros((hs, mw))) # generate matrix to be shown
    
    cv2.namedWindow('singleWH',cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('singleWH',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    for i in range(sqrtN):
        
        for j in range(sqrtN):
            
            matrix_i[:,(mw - hs) // 2 : (mw + hs) // 2] = 255 * wh.hadamard_ij(W, i, j, invert = False) 
            
            cv2.imshow('singleWH', matrix_i)
            
            cv2.waitKey(1000//1000)
            
    



