# Hough Lines in OpenCV

The hough lines method is a way of extracting lines from images. There are two ways to do this in OpenCV. The first is using a standard Hough transform using `cv2.HoughLines()`. This will return an array of [rho, theta] values. Which can then be used to draw the lines on the image if needed.

```
import cv2
import numpy as np

img = cv2.imread('building.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)


for i in range(0, len(lines) - 1):
    for rho,theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imshow('houghlines3.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

The `cv2.HoughLines()` function takes a binary image as it's image argument, so we'll start by doing canny edge detection.

```
img = cv2.imread('building.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
```

Now we can use `cv2.HoughLines()` to calculate the lines in the image. It takes several arguments. `HoughLines(image, rho, theta, threshold)` 

`image` is the binary source image. `rho` is the distance resolution of the accumulator in pixels. `threshold` is the accumulator threshold parameter. Only lines that reach this threshold will be returned.

Now we can calculate and draw the lines on the image. Since the lines are given in a `[rho theta]` format, we need to convert these values to cartesian coordinates, that way we can draw them with `cv2.line()`.

```
lines = cv2.HoughLines(edges,1,np.pi/180,250)

for i in range(0, len(lines) - 1):
    for rho,theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
```

Now show the image.

```
cv2.imshow('houghlines3.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

The other method is known as a probabilistic hough transform. In OpenCV this is calculated very similarly to a regular hough transform, using the `cv2.HoughLinesP()` function. This function takes all the same arguments as the `HoughLines()` function, but it is recommended that the threshold be lowered.

The `HoughLinesP()` function will return two endpoints of a line `[x1, y1, x2, y2]`, rather than a rho and theta. So these endpoints can be directly draw the lines on the image.

```
linesp = cv2.HoughLinesP(edges, 100, np.pi/180, 250)
for i in range(len(linesp) - 1):
    for x1, y1, x2, y2 in linesp[i]:
        cv2.line(img_copy,(x1,y1),(x2,y2),(0,255,0),2)
```
