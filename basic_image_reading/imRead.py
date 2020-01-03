import cv2

img = cv2.imread('messi5.jpg',1)

cv2.imshow('messi_img',img)

cv2.waitKey(0)
cv2.destroyAllWindows