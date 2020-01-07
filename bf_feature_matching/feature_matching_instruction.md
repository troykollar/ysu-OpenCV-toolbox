# Feature Matching in OpenCV

To use feature matching, it will be useful to view the images side by side. Matplotlib is useful for this amoung other things, so we'll start by installing that.

1. Install the dependencies using `sudo apt-get install python3-matplotlib`
2. Install Matplotlib using pip with `pip install matplotlib`

One method of feature matching in OpenCV is called brute force.

```
import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('avengers.jpg',cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('avengers_on_desk.jpg',cv2.IMREAD_GRAYSCALE)

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1, des2)

matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:25], None, flags=cv2.DrawMatchesFlags_DEFAULT)

plt.imshow(img3), plt.show()
```

To do feature matching, we will use ORB to gather feature descriptors. `orb = cv2.ORB_create()`

Using this ORB object, we will gather all the keypoints and descriptors from both objects.
```
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
```
Next we create a BFMatcher object with `bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)`. It's arguments are `normType` which specifies the type of distance measurement to be used. In our case `cv2.NORM_HAMMING` since that is the type of distance measurement used in ORB feature detection. The distance measurement should always match that of your feature detection. The other argument, crossCheck is `True`. This means that for keypoints to be considered a match, they must match both ways (i.e. the point on img1 matches the point on img2, AND the same point on img2 matches the same point on img1). This works as an alternative to Lowe's ratio test that would be used if using SIFT method. This will give more accurate results.

Now we'll use the bf object to match the descriptors, and sort the matches.
```
matches = bf.match(des1, des2)

matches = sorted(matches, key = lambda x:x.distance)
```

Finally we'll create `img3` using `cv2.drawMatches`, and show the matched images.
```
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:25], None, flags=cv2.DrawMatchesFlags_DEFAULT)

plt.imshow(img3), plt.show()
```