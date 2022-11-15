import cv2 
import numpy as np

def test_medthod(base_img_path,obj_img_path,method='all',threshold = 0.96): 
    # load base image 
    base_img = cv2.imread(base_img_path)

    # load object iamge
    obj_img = cv2.imread(obj_img_path,cv2.IMREAD_UNCHANGED)

    # get the wight and hight from face img 
    obj_w = obj_img.shape[1]
    obj_h = obj_img.shape[0]

    # methods
    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED,cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]
    methods_name = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF','cv2.TM_SQDIFF_NORMED']
 
    # test all methods to see what is best
    if method == 'all':
        
        for method in methods:
            img2 = base_img.copy()
            # run algorithm
            result = cv2.matchTemplate(base_img, obj_img,method)
            # get values (accuracy and postions) 
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # show result
            print("#########################")
            print(f'Using: {methods_name[method]} ')
            print(f'Min_value: {min_val}, Max_value: {max_val}, Min_location:{min_loc}, Max_location:{max_loc}')

            # show result with threshold settings
            yloc, xloc = np.where(result >= threshold)
            print(f"Threshold : {threshold} and result {len(xloc),len(yloc)}")
            print("#########################")
            print('\n')

    else:
        # run algorithm
        result = cv2.matchTemplate(base_img, obj_img,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # show result
        print("#########################")
        print(f'Min_value: {min_val}, Max_value: {max_val}, Min_location: {min_loc}, Max_location: {max_loc}')
        # show result with threshold settings
        yloc, xloc = np.where(result >= threshold)
        print(f"Threshold : {threshold} and result {len(xloc),len(yloc)}")
        print("#########################")
        print('\n')

def make_rectangle(base_img_path,obj_img_path,method,threshold):
    # load base image 
    base_img = cv2.imread(base_img_path)

    # load object iamge
    obj_img = cv2.imread(obj_img_path,cv2.IMREAD_UNCHANGED)

    # get the wight and hight from face img 
    obj_w = obj_img.shape[1]
    obj_h = obj_img.shape[0]

    # run algolithm
    result = cv2.matchTemplate(base_img, obj_img,method)

    # get values (accuracy and postions) 
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # make rectangle 
    # thereshold
    yloc, xloc = np.where(result >= threshold)
    
    
    # clear overlap rectangle 
    rectangles =  []
    for (x,y) in zip(xloc,yloc):
        rectangles.append([int(x), int(y), int(obj_w), int(obj_h)])
        rectangles.append([int(x), int(y), int(obj_w), int(obj_h)])

    # group rectangle
    # 1 = how many rects in group || 0.2 = how close 
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)  
    print(len(rectangles))

    # make rectangles
    for (x,y,obj_w,obj_h) in rectangles:
        cv2.rectangle(base_img, (x,y), (x + obj_w, y + obj_h), (0,255,255), 2)

    # show image
    cv2.imshow('Result', base_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

#test_medthod('base_img.jpg','poring_front_left.jpg',cv2.TM_CCORR_NORMED,0.96)

#make_rectangle('base_img.jpg','poring_front_left.jpg',cv2.TM_CCORR_NORMED,0.96)


