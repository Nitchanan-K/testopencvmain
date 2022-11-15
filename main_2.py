import cv2 
import numpy as np


def findClickPositions(base_img, obj_img, threshold = 0.96, debug_mode = None):
    
    obj_img = cv2.imread(obj_img)
    

    # get shape from img 
    obj_w = obj_img.shape[1]
    obj_h = obj_img.shape[0]

    # found result in case of using cv2.TM_CCORR_NORMED
    # base_img passing by realtime window capture
    method = cv2.TM_CCORR_NORMED
    result = cv2.matchTemplate(base_img, obj_img,method)


    # locations 
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    # fisrt make list fo [x , y, w, h] rectangles
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), obj_w, obj_h]
        # append it twice to make sure that it overlap
        rectangles.append(rect)
        rectangles.append(rect)

    # gourping rectagles
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    #print(rectangles)


    points = []
    
    if len(rectangles):
        print('found poring!!')
        
        
        line_color = (0,255,255)
        line_type = 2
        marker_color = (0,255,255)
        marker_type = cv2.MARKER_CROSS
        
        # loop over all the rectangles all draw it 
        for (x, y, w, h) in rectangles:
            
            # determine center positon
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # save the points 
            points.append((center_x,center_y))
            
            if debug_mode == 'rectangles':
                # determine box positions 
                top_left = (x , y)
                bottom_right = (x + w, y + h)
                # Draw the box 
                cv2.rectangle(base_img , top_left, bottom_right, line_color, line_type)
            elif debug_mode == 'points':
                cv2.drawMarker(base_img, (center_x,center_y), marker_color,marker_type)

            
        if debug_mode: 
            cv2.imshow('Matches', base_img)
            #cv2.waitKey()
        
    return points

points = findClickPositions('base_img.jpg','poring_front.png', debug_mode='rectangles')
print(points)