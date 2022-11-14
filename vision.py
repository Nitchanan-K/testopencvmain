import cv2 
import numpy as np
import os




def findClickPositions(base_img_path, obj_img_path, threshold = 0.96, debug_mode = None):
    
    base_img = cv2.imread(base_img_path)
    poring_front_img = cv2.imread(obj_img_path)

    poring_w = poring_front_img.shape[1]
    poring_h = poring_front_img.shape[0]

    result = cv2.matchTemplate(base_img, poring_front_img,cv2.TM_CCORR_NORMED)

    # Get the all the positions from the match result that exceed our threshold
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    print(locations)

    rectangles = []


findClickPositions('base_img.jpg','poring_front.png')