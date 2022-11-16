import cv2 
import numpy as np 
import os 
from time import time, sleep
import pyautogui
import pydirectinput
# from PIL import ImageGrab
from windowcapture import WindowCapture
from detection import Detection
from vision import Vision
from hsvfilter import HsvFilter
from threading import Thread
from bot import RagnarokBot, BotState

DEBUG = True

# Note the game window need to open first on screen before run main.py

# initialize the WindowCapture class
wincap = WindowCapture('Ragnarok')

# load the detector 
detector = Detection('poring_front_hsv.jpg')

# load an empty Vision class
vision_poring = Vision()

# initialize the bot object 
bot = RagnarokBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))
'''
# initialize the Vision class
vision_poring = Vision('poring_front_hsv.jpg')
'''

# initialize the trackbar window
vision_poring.init_control_gui()
# poring HSV filter
poring_hsv_filter = HsvFilter(0,0,0,179,255,255,255,0,0,25)

# global variable used to notify the main loop of when the-
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

# start window capture thread
wincap.start()
# start detection thread 
# param1 = threshold / param2 = max_results
detector.start(0.80,10)
# start bot thread
bot.start()

# loop start
loop_time = time()

while(True):
    # if we dont have a screenshot yet, dont run code below 
    if wincap.screenshot is None:
        continue

    # screenshot = wincap.get_screenshot() # best way
    # screenshot = ImageGrab.grab() ok way
    # screenshot = pyautogui.screenshot() slow way 

    # convert it to cv2 img inces not using window_capture function
        #screenshot = np.array(screenshot)
        #screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # ***IMPROTANT use .JPG*** 
    # best case poring_front_left //0.80(for pre-process image)
    
    # do pre-process the image for detections process.
    # give hsv_filter parameter to set the preset hsv setting
    # if not you do it manually
    processed_image = vision_poring.apply_hsv_filter(wincap.screenshot, poring_hsv_filter)

    # do object detections with processed_image.
    #rectangles = vision_poring.find(processed_image, threshold = 0.80)
    detector.update(processed_image)

    # update the bot with the data it needs
    if bot.state == BotState.INITIALIZING:
        # while bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does start
        targets = vision_poring.get_click_points(detector.rectangles)
        bot.update_targets(targets)
    elif bot.state == BotState.SEARCHING:
        # when searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. it also needs an updated screenshot
        # to verify the hover tooltip once it has moved the mouse to that position
        targets = vision_poring.get_click_points(detector.rectangles)
        bot.update_targets(targets)
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.MOVING:
        # when moving, we need fresh screenshots to determine when we've stopped moving
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.MINING:
        # nothing is needed while we wait for the mining to finish
        pass





    if DEBUG:
        # draw the detection results onto the original image (given screenshot imgae // given list of rects)
        output_image = vision_poring.draw_rectangles(wincap.screenshot, detector.rectangles)
        # display real time window capture (pre-process/output-image)
        #cv2.imshow('Processed', processed_image)
        cv2.imshow('Matches', output_image)

    # take bot actions (old one)**
    # run the function in a thread separate from main thread
    #if not is_bot_in_action:
       # is_bot_in_action = True
        #t = Thread(target=bot_actions, args=(detector.rectangles,))    
        #t.start()

    # check time / check FPS
    #print(f'FPS {(1 / (time() - loop_time))}')
    #loop_time = time()

    if cv2.waitKey(1) == ord('q'):
        wincap.stop()
        detector.stop()
        bot.stop()
        cv2.destroyAllWindows()
        break

print('Done.')