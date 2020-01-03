# Canny edge detection in OpenCV

Canny edge detection can be broken down into 5 steps.

1. Remove the noise on the image
2. Find the intensity of gradients on the image
3. Apply non-maximum suppression to get rid of spurious response to edge detection
4. Apply double threshold to determine potential edges
5. Track edges by hysteresis: Finalize the detection of edges by suppressing all the other edges that are weak and not connected to strong edges.

This process is simplified by OpenCV using the Canny function.

```
import cv2

img = cv2.imread("messi5.jpg", 0)
canny = cv2.Canny(img, 100, 200)

cv2.imshow('img',img)
cv2.imshow('canny',canny)

cv2.waitKey(0)
cv2.destroyAllWindows
```
This script will determine the edges in the `messi5.jpg` file.

To start, the line `img = cv2.imread("messi5.jpg", 0)` will be used to read the image. For this to work, either the image will need to be located in your current working directory, or you will need to specify the path. In this case the file is in our working directory.

`cv2.imread(filename, flags=None)` is the function used to read the images into the script. Some commonly used flags are 0 for grayscale, and 1 for color. There are many more flags that can be found in the OpenCV documentation.

The line `canny = cv2.Canny(img, 100, 200)` uses the `Canny` function to run the Canny edge detection algorithm on the image, and stores the resulting image in our variable `canny`. The `Canny` function has three required arguments, and several optional arguments.

`Canny(image, threshold1, threshold2, edges=None, apertureSize=None, L2gradient=None)`

`threshold1` refers to the lower threshold used in the algorithm, while `threshold2` refers to the upper threshold. They are upper and lower thresholds of the pixel gradients, put simply, the change in intensity at a specific pixel.

The `imshow` function is used to display the images. It takes two arguments, `imshow(winname, mat)`  

Where `winname` refers to a string that will be used as the name of the window, and `mat` which is the variable of the image to be displayed.