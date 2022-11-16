import cv2 
import numpy as np 
import os 

from time import time, sleep
import pyautogui
# from PIL import ImageGrab
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from threading import Thread


# Note the game window need to open first on screen before run main.py

# initialize the WindowCapture class
wincap = WindowCapture('Ragnarok')
# initialize the Vision class
vision_poring = Vision('poring_front_hsv.jpg')
# initialize the trackbar window
vision_poring.init_control_gui()
# poring HSV filter
hsv_filter = HsvFilter(0,0,0,179,255,255,255,0,0,25)

# global variable used to notify the main loop of when the
# bot actions have completed
is_bot_in_action = False 
 
# this function will be perform inside another thread
def bot_actions(rectangles):
    if len(rectangles) > 0:
        print('bot_ actions working')
        # garb first object in the list 
        # to click
        targets = Vision.get_click_points(rectangles)
        target = wincap.get_screen_position(targets[0]) # get the ture position
        pyautogui.moveTo(x=target[0], y=target[1])
        pyautogui.click()
        # wait 5 second for killing to complete
        sleep(5)

    # let the main loop know whem this process is completed
    global is_bot_in_action
    is_bot_in_action = False


loop_time = time()
while(True):

    screenshot = wincap.get_screenshot() # best way
    # screenshot = ImageGrab.grab() better way
    # screenshot = pyautogui.screenshot() slower way 

    # convert it to cv2 img inces not using window_capture function
        #screenshot = np.array(screenshot)
        #screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)


    # ***IMPROTANT use .JPG*** 
    # best case poring_front_left //0.96
    # point can use with bot

    # ore-process the image
    processed_image = vision_poring.apply_hsv_filter(screenshot, hsv_filter)

    # do object detections
    rectangles = vision_poring.find(processed_image, threshold = 0.80)
    
    # draw the detection results onto the original image (give screenshot imgae // give list of rects)
    output_image = vision_poring.draw_rectangles(screenshot, rectangles)

    # display real time window capture
    cv2.imshow('Processed', processed_image)
    cv2.imshow('Matches', output_image)

    # take bot actions
    # run the function in a thread separate from main thread
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_actions, args=(rectangles,))    
        t.start()


    # check time 
    print(f'FPS {(1 / (time() - loop_time))}')
    loop_time = time()

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break

print('Done.')