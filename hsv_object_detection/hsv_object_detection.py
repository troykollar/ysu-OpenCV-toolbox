import cv2
import numpy as np

def changeValue(x):
    print(x)

cv2.namedWindow('Tracking')
cv2.createTrackbar('H Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('H High', 'Tracking',0,255,changeValue)
cv2.createTrackbar('S Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('S High', 'Tracking',0,255,changeValue)
cv2.createTrackbar('V Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('V High', 'Tracking',0,255,changeValue)

while True:
    frame = cv2.imread('smarties.png')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    H_L = cv2.getTrackbarPos('H Low', 'Tracking')
    H_H = cv2.getTrackbarPos('H High', 'Tracking')
    S_L = cv2.getTrackbarPos('S Low', 'Tracking')
    S_H = cv2.getTrackbarPos('S High', 'Tracking')
    V_L = cv2.getTrackbarPos('V Low', 'Tracking')
    V_H = cv2.getTrackbarPos('V High', 'Tracking')
    lowerBound = np.array([H_L , S_L, V_L])
    upperBound = np.array([H_H, S_H, V_H])


    mask = cv2.inRange(hsv, lowerBound, upperBound)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask', mask)
    cv2.imshow('result', res)

    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()