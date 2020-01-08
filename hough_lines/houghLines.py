import cv2
import numpy as np

img = cv2.imread('building.jpg')
img_copy = cv2.imread('building.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,250)

for i in range(0, len(lines) - 1):
    for rho,theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

linesp = cv2.HoughLinesP(edges, 100, np.pi/180, 250)
for i in range(len(linesp) - 1):
    for x1, y1, x2, y2 in linesp[i]:
        cv2.line(img_copy,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow('houghlines()',img)
cv2.imshow('houghlinesp()', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()