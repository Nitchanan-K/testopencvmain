import cv2 
import numpy as np
import os

def findClickPositions(base_img_path, obj_img, threshold = 0.969, debug_mode = None):
    
    poring_front = cv2.imread('poring_front.png')
    
    poring_front = poring_front.shape[1]
    poring_front = poring_front.shape[0]

    result = cv2.matchTemplate(base_img, poring_front,cv2.TM_CCORR_NORMED)

    pass