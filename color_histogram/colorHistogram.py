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