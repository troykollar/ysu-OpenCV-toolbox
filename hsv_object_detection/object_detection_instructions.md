# Detecting objects using HSV colorspace

The simplest way to detect and track objects is using a range of HSV color values. The HSV colorspace is explained here https://www.lifewire.com/what-is-hsv-in-design-1078068.

Using OpenCV to track objects in the HSV colorspace is very simple. A range is specified for your H values, S values, and V values. The script below is what we'll use.

```
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
```

To find these ranges more easily, we start by creating trackbars. In lines 7-13, we create a window for trackbars, and the trackbars that will be in that window. These trackbars will be used to set the upper and lower bounds for our HSV ranges.

```
#Assign a function that prints the new value of the trackbar when its value is changed
def changeValue(x):
    pass

cv2.namedWindow('Tracking')
cv2.createTrackbar('H Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('H High', 'Tracking',0,255,changeValue)
cv2.createTrackbar('S Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('S High', 'Tracking',0,255,changeValue)
cv2.createTrackbar('V Low', 'Tracking',0,255,changeValue)
cv2.createTrackbar('V High', 'Tracking',0,255,changeValue)
```

As an example `cv2.createTrackbar('H Low', 'Tracking',0,255,changeValue)` will be used to find the lower threshold of our Hue range. 0 being the minimum, and 255 being the maximum.

The next thing to do is read the image and store a version of it in hsv format. This is done using `cv2.cvtColor`, which takes two arguments, the source image, and the colorspace to convert to. Since we are converting to HSV we use `cv2.COLOR_BGR2HSV` as our colorspace.

```
while True:
    frame = cv2.imread('smarties.png')

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

Next we use `getTrackbarPos` to assign the trackbar positions to variables. `getTrackbarPos` takes two arguments, the name of the trackbar, and the name of the window it is located in. Then we place those values into arrays using numpy.

```
lowerBound = np.array([H_L , S_L, V_L])
upperBound = np.array([H_H, S_H, V_H])
```

Now, we need to create a mask, i.e. a binary image that is white wherever the source image is within the HSV ranges.    `mask = cv2.inRange(hsv, lowerBound, upperBound)`. we will also create a result image to show what is detected using the mask. `res = cv2.bitwise_and(frame, frame, mask=mask)` To create this resulting image, we use the `bitwise_and` function. This will display the original image wherever the mask is white, and black otherwise.

From here, all that's left to do is display the images.

```
cv2.imshow('frame',frame)
cv2.imshow('mask', mask)
cv2.imshow('result', res)
```