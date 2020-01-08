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