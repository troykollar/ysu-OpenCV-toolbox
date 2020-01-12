import cv2
import numpy as np
import csv
import sys

if sys.argv[1] == None:
    noOutput = True
else:
    noOutput = False

if noOutput == False:
    outFilename = sys.argv[1]

refPoint = []       # List for each corner of the rectangle
lButtonDrag = False    # Says whether or not the user is currently dragging lbutton
rButtonDrag = False    # Says whether or not the user is currently dragging rbutton

def onClick(event, x, y, flags, param):
    #Grab global variables
    global refPoint, lButtonDrag, rButtonDrag, mask, mask_copy, image, image_copy
    if event == cv2.EVENT_LBUTTONDOWN:  # Once click is started
        refPoint.append((x,y))          # Append first point of the rectangle
        lButtonDrag = True                 # Indicate drawing has started

    if (lButtonDrag == True):               # while the user is dragging lButton
        if (event == cv2.EVENT_LBUTTONUP):  # if user releases
            refPoint.append((x,y))          # append the second rectangle corner
            mask_copy = mask.copy()
            image_copy = image.copy()
            lButtonDrag = False                # Indicate the user is no longer dragging lButton

            #Draw rectangle
            cv2.rectangle(image, refPoint[0], refPoint[1], (0, 255, 0), 2)
            cv2.rectangle(mask, refPoint[0], refPoint[1], (1), 0)

            refPoint.clear()    # Clear reference points so new rectangles can be drawn

        if (event == cv2.EVENT_MOUSEMOVE):  # While user is lButtonDrag, draw rectangle
            image = image_copy.copy()       # Revert to original image each mouse move, so rectangles don't overlap
            mask = mask_copy.copy()         # Revert to original mask each mouse move, so rectangles don't overlap

            #Draw rectangle
            cv2.rectangle(image, refPoint[0], (x,y), (0, 255, 0), 2)
            cv2.rectangle(mask, refPoint[0], (x,y), (1), -1)

def writeToCSV(image, filename : str):
    np.savetxt(filename, image, fmt='%1.0d', delimiter=',')

image = cv2.imread('board.jpg')
image_copy = image.copy()   # Create a copy of the image for drawing purposes
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', onClick)  # Assign the onClick function to the image
width, height = image.shape[:2]         # Get width and height of the image for mask

mask = np.zeros((width, height))        # Create mask
mask_copy = mask.copy()                 # Mask copy for drawing purposes

while True:
    cv2.imshow('Image', image)  # Show image
    cv2.imshow('mask', mask)    # Show mask
    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):             # If user presses r
        image = image_copy.copy()   # Revert to original copy of image
        refPoint.clear()            # Clear rectangle corners
        lButtonDrag = False            # Indicate the user is not lButtonDrag
    elif key == 27:     # 27 represents escape key 
        break

if noOutput == False:
    writeToCSV(mask, outFilename)

cv2.destroyAllWindows()