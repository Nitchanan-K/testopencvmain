import cv2 
import numpy as np 
import os 
from time import time
import pyautogui
from PIL import ImageGrab
from windowcapture import WindowCapture



wincap = WindowCapture('Ragnarok')


loop_time = time()
while(True):

    screenshot = wincap.get_screenshot() # best way
    # screenshot = ImageGrab.grab() better way
    # screenshot = pyautogui.screenshot() slower way 

    # convert it to cv2 img inces not using window_capture function
        #screenshot = np.array(screenshot)
        #screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    cv2.imshow('Computer Vision', screenshot)

    # check time 
    print(f'FPS {(1 / (time() - loop_time))}')
    loop_time = time()

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break



print('done')