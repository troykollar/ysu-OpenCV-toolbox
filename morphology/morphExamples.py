import cv2
import numpy as np
from matplotlib import pyplot as plt

baseImg = cv2.imread('j.png')
kernel = np.ones((5,5),np.uint8)    #5x5 array of 1's to be used as kernel

#erosion
erosionImg = cv2.erode(baseImg, kernel)

#dilation
dilationImg = cv2.dilate(baseImg, kernel)

#opening
openingImg = cv2.morphologyEx(baseImg, cv2.MORPH_OPEN, kernel)

#closing
closingImg = cv2.morphologyEx(baseImg, cv2.MORPH_CLOSE, kernel)

#morphological gradient
morphGradient = cv2.morphologyEx(baseImg, cv2.MORPH_GRADIENT, kernel)

#tophat
tophat = cv2.morphologyEx(baseImg, cv2.MORPH_TOPHAT, kernel)

#black hat
blackhat = cv2.morphologyEx(baseImg, cv2.MORPH_BLACKHAT, kernel)

figure = plt.figure()

def add_image(plot_position, src, title):
    figure.add_subplot(2,4,plot_position)
    plt.imshow(src)
    plt.title(title)

# Show base image
add_image(1, baseImg, 'Base Image')

# Show erosion image
add_image(2, erosionImg, 'Erosion')

#Show dilation image
add_image(3, dilationImg, 'Dilation')

#Show opening image
add_image(4, openingImg, 'Opening')

#Show closing iamge
add_image(5, closingImg, 'Closing')

#Show morphological gradient
add_image(6, morphGradient, 'Gradient')

#Show top hat
add_image(7, tophat, 'Top Hat')

#Show black hat
add_image(8, blackhat, 'Black Hat')

plt.show()
