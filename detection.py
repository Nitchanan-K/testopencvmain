import cv2 
import numpy as np
from threading import Thread,Lock

class Detection:

    # threading properties 
    stopped = True
    lock = None
    rectangles = []
    # properties 
    obj_img = None
    obj_w = 0
    obj_h = 0 
    method = None
    screenshot = None
    threshold = 0
    max_results = 0

    # constructoe
    def __init__(self, obj_img_path,method=cv2.TM_CCORR_NORMED):
        # create a thread lock object 
        self.lock = Lock()

        # load image 
        self.obj_img = cv2.imread(obj_img_path,cv2.IMREAD_UNCHANGED)
        # get shape from img 
        self.obj_w = self.obj_img.shape[1]
        self.obj_h = self.obj_img.shape[0]
        # method 
        self.method = method

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self,threshold,max_results):
        self.stopped = False
        t = Thread(target=self.run,args=(threshold,max_results))
        t.start()


    def stop(self):
        self.stopped = True

    def run(self,threshold,max_results):
        # 
        while not self.stopped:
            if not self.screenshot is None:
            ###############################
                # do object detection
                result = cv2.matchTemplate(self.screenshot, self.obj_img, self.method)
                
                # hold value ***
                #threshold = 0.80 
                #max_results= 10

                # locations found with >= threshold
                locations = np.where(result >= threshold)
                locations = list(zip(*locations[::-1]))
                
                # if we found no results, return now. this reshape of the empty array allows us to 
                # concatenate together results without causing an error
                if not locations:
                    rectangles = np.array([], dtype=np.int32).reshape(0, 4)
                
                # fisrt make list fo [x , y, w, h] rectangles
                rectangles = []
                for loc in locations:
                    rect = [int(loc[0]), int(loc[1]), self.obj_w, self.obj_h]
                    # append it twice to make sure that it overlap
                    rectangles.append(rect)
                    rectangles.append(rect)
                
                # gourping rectagles
                rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
                # print(rectangles)

                # for performance reasons, return a limited number of results.
                # these aren't necessarily the best results.
                if len(rectangles) > max_results:
                    print('Warning: too many results, raise the threshold.')
                    rectangles = rectangles[:max_results]
            ###############################

                # lock the thread while updating the rectangles 
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()