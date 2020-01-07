import numpy as np
import cv2
colorImg = cv2.imread('opencv-logo.png',1) #read image grayscale
grayImg = cv2.cvtColor(colorImg, cv2.COLOR_BGR2GRAY)
grayImg = cv2.medianBlur(grayImg,5) #Smooth image
circles = cv2.HoughCircles(grayImg,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)
circles = np.uint16(np.around(circles))
# draw the circles
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(colorImg, (i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(colorImg,(i[0],i[1]),2,(0,0,255),3)
cv2.imshow('detected circles',colorImg)
cv2.waitKey(0)
cv2.destroyAllWindows()