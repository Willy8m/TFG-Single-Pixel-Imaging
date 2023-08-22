# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:38:19 2023

@author: guill
"""

from src import CameraWatcher
from PIL import Image
import numpy as np
import cv2
import time


cams = CameraWatcher(1)
cams.watch_camera(("192.168.1.83", 8000), shutter_speed = 20000)

fps_measure = True

if fps_measure:
    
    c = 0
    capture_times = []
    t_ini = time.time()
    
while True:
    
    t1 = time.time()
    
    img_buffer = cams.get_image(0) # capture
    Jpeg_file = Image.open(img_buffer) # load image
    data = np.asarray(Jpeg_file) # convert to numpy array
    cv2.imshow('frame', data)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
    
    if fps_measure:
        
        c += 1
        t = time.time() - t1
        capture_times.append(t)

if fps_measure:
    
    t_fin = time.time()
    print('time', t_fin-t_ini, '\nN:   ', c)
    print('fps: ', c / (t_fin-t_ini))
    print('maxvalue:', np.max(data))

cams.close()

