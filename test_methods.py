import cv2 
import numpy as np

base_img = cv2.imread('base_img.jpg')

poring_back = cv2.imread('poring_back.png')
#poring_back = cv2.cvtColor(poring_back, cv2.COLOR_RGB2GRAY)

poring_front = cv2.imread('poring_front.png')
#poring_front = cv2.cvtColor(poring_front , cv2.COLOR_RGB2GRAY)

# get the wight and hight from face img 
w = poring_front.shape[1]
h = poring_front.shape[0]

# methods
methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED,cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]

# test all methods to see what is best 
'''
for method in methods:
    img2 = base_img.copy()
    result = cv2.matchTemplate(base_img, poring_front,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val, max_val, min_loc, max_loc)
'''

# method 4
result = cv2.matchTemplate(base_img, poring_front,cv2.TM_CCORR_NORMED)


# threshold
threshold = .96

yloc, xloc = np.where(result >= threshold)
# return manys location that matcted
print(len(xloc),len(yloc))

# locations 
locations = np.where(result >= threshold)
locations = list(zip(*locations[::-1]))
print(locations)

# make rectagle in forloop 
'''
for (x,y) in zip(xloc,yloc):
    cv2.rectangle(base_img, (x,y), (x + w, y + h), (0,255,255), 2)
'''
'''
for loc in location :
    top_left =loc 
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2. rectangle(base , top_left, bottom_right, line_color, line_type)
'''
 


# what is a rectangle?
# x, y ,w h
rectangles =  []
for (x,y) in zip(xloc,yloc):
    rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles.append([int(x), int(y), int(w), int(h)])

print(len(rectangles))

rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
print(len(rectangles))


# make reactangles with group
for (x,y,w,h) in rectangles:
    cv2.rectangle(base_img, (x,y), (x + w, y + h), (0,255,255), 2)

    cv2.imshow('Result', base_img)
cv2.waitKey()
cv2.destroyAllWindows()