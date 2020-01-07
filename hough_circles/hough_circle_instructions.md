# Detecting Circles with OpenCV

OpenCV uses the Hough Gradient Method of detecting circles. Which is explained [here](https://en.wikipedia.org/wiki/Hough_transform). The code is very simple.

```
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
    cv2.circle(colorImg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(colorImg,(i[0],i[1]),2,(0,0,255),3)
cv2.imshow('detected circles',colorImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
The Hough Gradient method works using a grayscale input image, and smoothing the image can help with detection. Most of it's arguments are self-explanitory, except `param1` and `param2`. `param1` is the upper threshold that is passed to the canny edge detector within the hough_circles function. The lower threshold will automatically be half of this value. `param2`  is the accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected. Circles, corresponding to the larger accumulator values, will be returned first.
```
colorImg = cv2.imread('opencv-logo.png',1) #read image grayscale
grayImg = cv2.cvtColor(colorImg, cv2.COLOR_BGR2GRAY)
grayImg = cv2.medianBlur(grayImg,5) #Smooth image
circles = cv2.HoughCircles(grayImg,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)
```
The `cv2.circles()` function will calculate the circles in the format of a list with `circle_index[x_coordinate, y coordinate, radius]`, which makes them easy to input this information into the `cv2.circle()` drawing function.

All that we need to do now is draw the circles on the image. We'll do this using the `cv2.circle()` function. `cv2.circle()` takes integers for the position and radius arguments. So we first convert the circles list into `uint16` format.

```
circles = np.uint16(np.around(circles))
# draw the circles
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(colorImg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(colorImg,(i[0],i[1]),2,(0,0,255),3)
```

And finally display the image with the circles drawn on it.
```
cv2.imshow('detected circles',colorImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

