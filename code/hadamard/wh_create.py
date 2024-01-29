#!/usr/bin/env python3

#-----------------------------------------
# CREATION OF WALSH-HADAMARD MATRICES
#-----------------------------------------


import numpy as np
import matplotlib.pyplot as plt
import cv2


def xnor(a,b,maxi,mini):
    
    c= np.empty(a.shape)
    
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            
            if a[i,j]==b[i,j]:
                c[i,j]= np.uint8(maxi)
            else:
                c[i,j]= np.uint8(mini)
                
    return c
    
    

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



#-----------------------------------------------------
# SET THE EXPERIMENTAL PARAMETERS

size=256 # size of the hadamard matrix displayed on the SLM -> multiple of 'res'

maxi=1 # graylevel with maximum transmission
mini=0 # graylevel with minimum transmission



#--------------------------------------------------------
# GENERATE A HADAMARD MATRIX

order = 8 # set the order (which compromises resolution of the reconstruction)

H= hadamard(order) # contains disordered Walsh functions

res= H.shape[0] # width of the matrix



#--------------------------------------------------------
# EXTRACT WALSH FUNCTIONS FROM ITS ROWS


# order the functions
 
W= np.uint8( np.zeros((H.shape))) # will contain ordered Walsh functions
n= np.uint8( np.empty((res)))


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
            
    

#------------------------------------------------------
# CROSS WALSH FUNCTIONS TO GET WALSH-HADAMARD MATRICES

N= res**2 # number of matrices

WH0= np.uint8( np.empty((res, res, N))) # 1 and 0
WH1= np.uint8( np.empty((res, res, N))) # 0 and -1


kont= 0

for i in range(res):
    for j in range(res):
            
        X, Y= np.meshgrid( W[i,:], W[j,:] )
            
        WH0[:,:,kont]= xnor(X, Y, maxi, mini)
        WH1[:,:,kont]= xnor(X, Y, mini, maxi)
        
        kont += 1
        if kont%(N//10) == 0:
            print(kont//(N/101),'%')
            

filename0 = 'wh0_0_' + str(2**(order-1))
filename1 = 'wh1_1_' + str(2**(order-1))

np.save(filename0, WH0)
np.save(filename1, WH1) 

# PACKBITS

filename0 += '_p' 
filename1 += '_p'

WH0 = np.packbits(WH0)
WH1 = np.packbits(WH1)

np.save(filename0, WH0)
np.save(filename1, WH1) 
   


"""    
#---------------------------------------
# ADJUST PATTERNS TO DISPLAY SIZE

WH0= np.load('wh0_0_32.npy')
WH1= np.load('wh1_1_32.npy')

N= WH0.shape[2]

# reduce the maximum intensity
WH0= maxi*WH0
WH1= maxi*WH1

WH0_pad= np.empty((size, size, N))
WH1_pad= np.empty((size, size, N))


for k in range(N):
	
	WH0_pad[:,:,k]= cv2.resize(WH0[:,:,k],(size,size),interpolation=cv2.INTER_NEAREST)
	WH1_pad[:,:,k]= cv2.resize(WH1[:,:,k],(size,size),interpolation=cv2.INTER_NEAREST)
        
np.save('wh0_gray_n32_s256', WH0_pad)
np.save('wh1_gray_n32_s256', WH1_pad)    



plt.figure()
plt.subplot(221)
plt.imshow(WH0[:,:,100])
plt.subplot(222)
plt.imshow(WH0_pad[:,:,190])  
plt.subplot(223)
plt.imshow(WH1[:,:,240])  
plt.subplot(224)
plt.imshow(WH1_pad[:,:,14])   
plt.show()
"""
