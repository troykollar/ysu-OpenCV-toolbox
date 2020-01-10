import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

def changeValue(x):
    pass

cap = cv2.VideoCapture('box.mp4')
cv2.namedWindow('Tracking')
cv2.createTrackbar('H Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('H High', 'Tracking',0,255,changeValue)
cv2.createTrackbar('S Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('S High', 'Tracking',0,255,changeValue)
cv2.createTrackbar('V Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('V High', 'Tracking',0,255,changeValue)
playVideo = True

#Create cv2.WINDOW_NORMAL windows so we can resize them later
cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)
cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)

while (cap.isOpened()):
    #If we haven't quit the video, read the next frame
    if playVideo == True:
        ret, frame = cap.read()
    if ret == True:
        H_L = cv2.getTrackbarPos('H Low', 'Tracking')
        H_H = cv2.getTrackbarPos('H High', 'Tracking')
        S_L = cv2.getTrackbarPos('S Low', 'Tracking')
        S_H = cv2.getTrackbarPos('S High', 'Tracking')
        V_L = cv2.getTrackbarPos('V Low', 'Tracking')
        V_H = cv2.getTrackbarPos('V High', 'Tracking')
        lowerBound = np.array([30, 0, 0])
        upperBound = np.array([120, 255, 255])

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        #get hsv version of video
        mask = cv2.inRange(hsv, lowerBound, upperBound)     #get mask
        result = cv2.bitwise_and(frame,frame, mask=mask)    #bitwise_and with mask to get resulting image
        edged = cv2.Canny(result,30,150)                    #Calculate edges

        #Calculate contours to show edges of our tracked image
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        #Draw the contours onto the frame
        cv2.drawContours(frame, contours, -1, (0,255,0),3)

        cv2.imshow('Mask', mask)        #Show mask
        cv2.resizeWindow('Mask', 640, 480)
        cv2.imshow('Contours', frame)   #Show image with contours drawn
        cv2.resizeWindow('Contours', 640,480)

        key = cv2.waitKey(5)
        if cv2.waitKey(10) & 0xFF == ord('p'):
            playVideo = not playVideo

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
