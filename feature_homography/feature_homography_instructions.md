# Feature Homography

Feature Homography is a way of identifying objects in images using the matching of features.

OpenCV provides a tutorial in their documentation at https://docs.opencv.org/master/d1/de0/tutorial_py_feature_homography.html, however, this tutorial is using the SIFT feature detection algorithm, which is patented, and requires payment to use. We will be using the ORB feature detection algorithm.

```
import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

img1 = cv2.imread('box.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('box_in_scene.png', cv2.IMREAD_GRAYSCALE)

#ORB detector
orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)

matches = bf.match(des1, des2)
matches = sorted(matches, key= lambda x:x.distance)

if len(matches) > MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape[:2]
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print("Not enough matches".format(len(matches), MIN_MATCH_COUNT))
    print(len(matches))
    matchesMask = None

img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches,None)
plt.imshow(img3, 'gray'),plt.show()
```
First, the images must be read in grayscale, or converted to grayscale e.g. `img1 = cv2.imread('box.png', cv2.IMREAD_GRAYSCALE)`

Next we go through a similar feature matching process as that in [bf_feature_matching](../bf_feature_matching/feature_matching_instruction.md).
```
#ORB detector
orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)

matches = bf.match(des1, des2)
matches = sorted(matches, key= lambda x:x.distance)
```