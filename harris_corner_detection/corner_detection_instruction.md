# Harris Corner Detection

Corners in an image are basically regions in the image with large variations of intensity in all directions.

Finding corners in OpenCV can be done using `cv2.cornerHarris()`.

It takes 4 arguments.

1. `img` - Input image. It should be grayscale and float32 type.
2. `blockSize` - It is the size of neighbourhood considered for corner detection. Neighbourhood size is a (`blockSize` x `blockSize`) area around each pixel.
3. `ksize` - Aperture parameter of the Sobel derivative used.
    - The ksize parameter determines the size of the Sobel kernel (3x3, 5x5, etc..). As the size increases, more pixels are part of each convolution process and the edges will get more blurry.
4. `k` - Harris detector free parameter in the equation.
    - The `k` parameter should be between 0.04 and 0.06. It is basically a tradeoff of whether you are willing to miss some corners to ensure fewer "false" corners. A lower `k` will produce more "false corners" but is less likely to miss any real corners, while a higher `k` will produce fewer "false" corners, but may miss some real corners.

The `cornerHarris()` function will return a grayscale image which has very small values for flat areas, negative values for edges, and larger values for corners. Thus, it can be used to highlight corners on the original image.

Our script to detect the corners on `left01.jpg` :

```
import numpy as np
import cv2 as cv
filename = 'left01.jpg'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv.imshow('dst',img)
cv.imshow('corner',dst)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
```

Here, the image is read and converted to a grayscale float32 image:
```
filename = 'left01.jpg'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = np.float32(gray)
```
Next, the `cornerHarris()` function is run on the image:
`dst = cv.cornerHarris(gray,2,3,0.04)`

And finally, a ROI (region of image) operation is performed on the original image. `img[dst>0.01*dst.max()]=[0,0,255]` This describes the regions of `img` where the value of `dst` is greater than 0.01 (i.e. the corners). Those regions are set to a BGR value of `[0,0,255]` which changes the color of those regions to red.

The final images are then displayed.
```
cv.imshow('dst',img)
cv.imshow('corner',dst)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
```