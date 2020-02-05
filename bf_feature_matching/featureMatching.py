import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('DogBone3-1.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('Overmold1-1.jpg', cv2.IMREAD_GRAYSCALE)

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1, des2)

matches = sorted(matches, key=lambda x: x.distance)

img3 = cv2.drawMatches(img1,
                       kp1,
                       img2,
                       kp2,
                       matches,
                       None,
                       flags=cv2.DrawMatchesFlags_DEFAULT)

plt.imshow(img3)
plt.show()