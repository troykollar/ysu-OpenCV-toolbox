# Reading and displaying an image using OpenCV

Reading and displaying images in OpenCV is very simple.

```
import cv2

img = cv2.imread('messi5.jpg',1)

cv2.imshow('messi_img',img)

cv2.waitKey(0)
cv2.destroyAllWindows
```

The line `img = cv2.imread('messi5.jpg',1)` reads the image and stores it in the `img` variable. The '1' used as the second argument of the `imread` function is known as a flag. This determines "how" the image will be read, i.e. 1 will read as color, and 0 will read as grayscale. There are more flags that can be found in the OpenCV documentation.

The `imshow` command displays the image on the screen. It has two arguments. The first being `winname` or the string that gives title of the window, in our case `'messi_img'`. The other argument being the variable containing the image to be displayed, `img` in our case.

The `waitKey()` function tells the program to keep the image displayed for a duration specified as a number in the argument. Passing 0 as an argument will keep the image open until the user presses Esc.

Finally `cv2.destroyAllWindows` will close all the windows that are open after the `waitKey` function has completed.