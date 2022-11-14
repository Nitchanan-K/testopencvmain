import cv2 
import numpy as np

base_img = cv2.imread('base_img.jpg', cv2.IMREAD_UNCHANGED)
#base = cv2.cvtColor(base, cv2.COLOR_RGB2GRAY)

poring_back = cv2.imread('poring_back.png', cv2.IMREAD_UNCHANGED)
poring_back = cv2.cvtColor(poring_back, cv2.COLOR_RGB2GRAY)

poring_front = cv2.imread('poring_front.png', cv2.IMREAD_UNCHANGED)
poring_front = cv2.cvtColor(poring_front , cv2.COLOR_RGB2GRAY)

# methods
methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED,cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]

for method in methods:
    img2 = base_img.copy()
    result = cv2.matchTemplate(base_img, poring_front, cv2.TM_CCOEFF_NORMED)


# retrun match result 
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)




print(max_loc)
print(max_val,min_val)

# get the wight and hight from face img 
w = poring_front.shape[1]
h = poring_front.shape[0]

# make rectagle 
cv2.rectangle(base_img,max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)

# threshold
threshold = .50
yloc, xloc = np.where(result >= threshold)
# return manys location that matcted
print(len(xloc),len(yloc))

# make rectagle in forloop 
for (x,y) in zip(xloc,yloc):
    cv2.rectangle(base_img, (x,y), (x + w, y + h), (0,255,255), 2)


cv2.imshow('Base',base_img)
cv2.imshow('Result', result)

cv2.waitKey()
cv2.destroyAllWindows()




