# Image Histograms in OpenCV

Image histograms can be used to analyze an image and see which colors, intensties, hues, etc. that are most common in an image. This is useful because it can be useful to determine if two images are similar based on their color makeup.

Image histograms are made in OpenCV using `cv2.calcHist()`.

First we'll make a grayscale histogram. This will help us to analyze the frequency of intensities in the image.

## Grayscale Histogram

Obviously, we'll need to first read the image in grayscale. `img = cv2.imread('butterfly.jpg', cv2.IMREAD_GRAYSCALE)`

Then, we can calculate the histogram. The `cv2.calcHist()` function has 5 required arguments. `images`, a list of the images to be calculated. We are using only one image, so we'll wrap our image variable as a list. 

`channels` is a list of the color channels to be calculated, for a grayscale image it is just `[0]`. 

`mask` if you wanted to do the histogram on a specific part of the image, you would create a mask of that area, and use that as your argument. Since we are doing the entire image we will use `None`.

`histSize` is the size of the histogram, this can vary for other colorspaces, but will be `[256]` for grayscale.

`ranges` is the range to be used for the histogram, for grayscale it will be `[0, 256]`

Calculating and showing the histogram using `matplotlib` will look like:

```
import cv2
from matplotlib import pyplot as plt

#Read grayscale image
img = cv2.imread('butterfly.jpg', cv2.IMREAD_GRAYSCALE)

#Calculate gray histogram
grayHist = cv2.calcHist([img], [0], None, [256], [0, 256])

#Show grayscale image
figure = plt.figure()
figure.add_subplot(1,2,1)
plt.imshow(img, cmap='gray')

#Show histogram
figure.add_subplot(1,2,2)
plt.plot(grayHist)

plt.show()
```

## Color Histogram

Creating a color histogram is nearly as simple. The difference being that each channel needs to be calculated individually, with each channel being specified in the `channel` argument of the `cv2.calcHist()` function.

```
import cv2
from matplotlib import pyplot as plt

#Read img in BGR format
img = cv2.imread('WindowsLogo.jpg')

#Convert to rgb
rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#Show image
figure = plt.figure()
figure.add_subplot(1,2,1)
plt.imshow(rgbImg)

figure.add_subplot(1,2,2)
#Get red channel in histogram
blueHist = cv2.calcHist([rgbImg], [0], None, [256], [0, 256])
plt.plot(blueHist, color='r')

#Get green channel in histogram
greenHist = cv2.calcHist([rgbImg], [1], None, [256], [0, 256])
plt.plot(greenHist, color='g')

#Get blue channel in histogram
redHist = cv2.calcHist([rgbImg], [2], None, [256], [0, 256])
plt.plot(redHist, color='b')

plt.show()
```
