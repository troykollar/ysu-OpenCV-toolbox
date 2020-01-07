# Feature Homography

Feature Homography is a way of identifying objects in images using the matching of features.

OpenCV provides a tutorial in their documentation at https://docs.opencv.org/master/d1/de0/tutorial_py_feature_homography.html, however, this tutorial is using the SIFT feature detection algorithm, which is patented, and requires payment to use. We will be using the ORB feature detection algorithm.

```
import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

queryImg = cv2.imread('box.png', cv2.IMREAD_GRAYSCALE)
trainImg = cv2.imread('box_in_scene.png', cv2.IMREAD_GRAYSCALE)

#ORB detector
orb = cv2.ORB_create(edgeThreshold=32, patchSize=32)

#detect and compute keypoints, and descriptors of both query and train images
kpQuery, desQuery = orb.detectAndCompute(queryImg, None)
kpTrain, desTrain = orb.detectAndCompute(trainImg, None)

matcher = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)

matches = matcher.match(desQuery, desTrain)

src_pts = np.zeros((len(matches),2), dtype=np.float32)  #create list of zeros of type float32
dst_pts = np.zeros((len(matches),2), dtype=np.float32)

for i, match in enumerate(matches):
    src_pts[i, :] = kpQuery[match.queryIdx].pt  #gives index of descriptor in query descriptors
    dst_pts[i, :] = kpTrain[match.trainIdx].pt  #gives index of descriptor in training descriptors

#Homography matrix, Mask
hgraphyMatrix, mask = cv2.findHomography(src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=5)
matchesMask = mask.ravel().tolist   # determine if points are in mask to avoid drawing points outside of mask

height, width = queryImg.shape # .shape always returns height, width, and channels

pts = np.float32([ [0,0], [0,height - 1], [width - 1, height -1], [width - 1,0] ]).reshape(-1,1,2)
dst = cv2.perspectiveTransform(pts, hgraphyMatrix)

#Draw outline around matched image
trainImg = cv2.polylines(trainImg, [np.int32(dst)], isClosed=True, color=255, thickness=3, lineType=cv2.LINE_AA)

matchLinesImg = cv2.drawMatches(queryImg, kpQuery, trainImg, kpTrain, matches, None, (0,255,0))
plt.imshow(matchLinesImg)
plt.show()
```

First we need to use an ORB detector to detect keypoints and calculate the descriptors for said keypoints.
```
#ORB detector
orb = cv2.ORB_create(edgeThreshold=32, patchSize=32)

#detect and compute keypoints, and descriptors of both query and train images
kpQuery, desQuery = orb.detectAndCompute(queryImg, None)
kpTrain, desTrain = orb.detectAndCompute(trainImg, None)
```

Now we use a brute force matcher (as shown in [bf_feature_matching](../bf_feature_matching)) to find matches of the keypoints on the query image and train image.

```
matcher = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)

matches = matcher.match(desQuery, desTrain)
```

Now we initiate `numpy` arrays filled with zeros. These will then be filled with the indexes from our query image to make a `src_pts` array, and indexes from the train image to make the `dst_pts` array.

```
src_pts = np.zeros((len(matches),2), dtype=np.float32)  #create list of zeros of type float32
dst_pts = np.zeros((len(matches),2), dtype=np.float32)

for i, match in enumerate(matches):
    src_pts[i, :] = kpQuery[match.queryIdx].pt  #gives index of descriptor in query descriptors
    dst_pts[i, :] = kpTrain[match.trainIdx].pt  #gives index of descriptor in training descriptors
```

Next we use `cv2.findHomography` to find the homography matrix and the mask. The more important thing here is the homography matrix, this is the (3x3) matrix that is calculated to find the transformation that was done on our keypoints. From this matrix, the program will be able to highlight the queryImg (Image we are searching for) within the trainImg (Image we are searching in).

The mask can be used to exclude matches from the drawing that are not included on the actual matched object, but we will not be doing this here.

```
#Homography matrix, Mask
hgraphyMatrix, mask = cv2.findHomography(src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=5)
matchesMask = mask.ravel().tolist   # determine if points are in mask to avoid drawing points outside of mask
```

Next we'll get the height and width of the query image, and have it transformed based on the homography matrix

```
height, width = queryImg.shape # .shape always returns height, width, and channels

pts = np.float32([ [0,0], [0,height - 1], [width - 1, height -1], [width - 1,0] ]).reshape(-1,1,2)
dst = cv2.perspectiveTransform(pts, hgraphyMatrix)
```

Now, we can use `cv2.polyLines()` and the dst we found from the `cv2.perspectiveTransform()` to draw an outline around the matched object.

```
#Draw outline around matched image
trainImg = cv2.polylines(trainImg, [np.int32(dst)], isClosed=True, color=255, thickness=3, lineType=cv2.LINE_AA)
```

Finally, we'll draw the matches from the two images, and display them next to each other.

```
matchLinesImg = cv2.drawMatches(queryImg, kpQuery, trainImg, kpTrain, matches, None, (0,255,0))
plt.imshow(matchLinesImg)
plt.show()
```