# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:43:08 2023

@author: guill
"""

#-----------------------------------------
# CREATION OF WALSH-HADAMARD MATRICES
#-----------------------------------------


import numpy as np
import matplotlib.pyplot as plt

def out_pr(a,b):
    
    a1=a.shape[0]
    a2=a.shape[1]
    b1=b.shape[0]
    b2=b.shape[1]
    
    c= np.empty((a1*b1,a2*b2))
    
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            
            ia= np.uint8(i/b1)
            ja= np.uint8(j/b2)
            ib= np.uint8(i%b1)
            jb= np.uint8(j%b2)
            
            c[i,j] = a[ia,ja] * b[ib,jb]
            
    return c



def hadamard(n): # lehengo beste_hadamard
    
    if n==1 or n==2:
        m= n
    else:
        m= (n-2)*4
    
    
    H2= np.array([[1,1],[1,-1]]) # beste bat izen leike
    H= H2
    
    mi=m
    
    while mi>2:
        
        H= out_pr(H,H2) # the order matters
        
        mi-=4
    
    return np.uint8(H)

def W(order): # create ordered walsh functions

    #--------------------------------------------------------
    # GENERATE A HADAMARD MATRIX
   
    H= hadamard(order) # contains disordered Walsh functions
    
    res= H.shape[0] # width of the matrix
    
    
    
    #--------------------------------------------------------
    # EXTRACT WALSH FUNCTIONS FROM ITS ROWS
    
    
    # order the functions
     
    W= np.uint8( np.zeros((H.shape))) # will contain ordered Walsh functions
    n= np.uint16( np.empty((res)))
    
    
    # count the jumps of each Walsh function
    
    for k in range(res):
        
        r= H[k, 0]
        nk= 0
        
        for i in range(res):
            
            if H[k,i] != r:
                nk += 1
                
            r= H[k,i]
            
        n[k]= nk
        
        
        
    # fill the W matrix with Walsh functions
    # with ascendent number os jumps from -1 to 1 or vice versa
        
    num= 0
    
    while num < res:
        
        for k in range(res):
            
            if n[k] == num:
                
                W[num,:]= H[k,:]
                
        num += 1
    
    # Make true false array
    W //= 255
    
    return W
                

    
def hadamard_ij(W, i, j, invert): # Creates and returns the ijth wh matrix 
    
    X, Y = np.meshgrid( W[i,:], W[j,:] )
    
    WH0 = np.logical_xor(X, Y)
    
    if not invert:
        
        WH0 = np.logical_not(WH0)
    
    return WH0
    

WH_matrix = hadamard(4)
WH_ordered = W(4)
WH_vector = hadamard_ij(W = WH_ordered, i = 1, j = 3, invert = True)


plt.figure()
plt.imshow(WH_vector)
plt.axis('off')
plt.tight_layout()
         



plt.figure()
plt.subplot(131)
plt.imshow(WH_matrix)
plt.axis('off')
plt.subplot(132)
plt.imshow(WH_ordered)
plt.axis('off')
plt.subplot(133)
plt.imshow(WH_vector)
plt.axis('off')
plt.tight_layout()
         
 
