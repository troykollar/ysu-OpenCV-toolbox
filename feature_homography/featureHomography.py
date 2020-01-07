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