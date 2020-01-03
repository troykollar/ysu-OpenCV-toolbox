import cv2

img = cv2.imread("messi5.jpg", 0)
canny = cv2.Canny(img, 100, 200)

cv2.imshow('img',img)
cv2.imshow('canny',canny)

cv2.waitKey(0)
cv2.destroyAllWindows