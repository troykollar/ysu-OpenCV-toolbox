import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("ImgFile", type=str,
                    help="The filename (and location if not in the same folder) of the image.")
parser.add_argument("OutFile", type=str,
                    help="The desired name of the csv output file (including .csv extension)")

ARGS = parser.parse_args()

IMG_FILE_NAME = ARGS.ImgFile
OUTPUT_FILE_NAME = ARGS.OutFile

refPoint = []       # List for each corner of the rectangle
lButtonDrag = False    # Says whether or not the user is currently dragging lbutton
rButtonDrag = False    # Says whether or not the user is currently dragging rbutton

def on_click(event, x, y, flags, param):
    #Grab global variables
    global refPoint, lButtonDrag, rButtonDrag, mask, mask_copy, image, image_copy
    if event == cv2.EVENT_LBUTTONDOWN:  # Once click is started
        refPoint.append((x, y))          # Append first point of the rectangle
        lButtonDrag = True                 # Indicate drawing has started

    if lButtonDrag:               # while the user is dragging lButton
        if event == cv2.EVENT_LBUTTONUP:  # if user releases
            refPoint.append((x, y))          # append the second rectangle corner
            mask_copy = mask.copy()
            image_copy = image.copy()
            lButtonDrag = False                # Indicate the user is no longer dragging lButton

            #Draw rectangle
            cv2.rectangle(image, refPoint[0], refPoint[1], (0, 255, 0), 2)
            cv2.rectangle(mask, refPoint[0], refPoint[1], (1), 0)

            refPoint.clear()    # Clear reference points so new rectangles can be drawn

        if event == cv2.EVENT_MOUSEMOVE:  # While user is lButtonDrag, draw rectangle
            image = image_copy.copy()       # Revert to original image each mouse move, so rectangles don't overlap
            mask = mask_copy.copy()         # Revert to original mask each mouse move, so rectangles don't overlap

            #Draw rectangle
            cv2.rectangle(image, refPoint[0], (x, y), (0, 255, 0), 2)
            cv2.rectangle(mask, refPoint[0], (x, y), (1), -1)

def write_to_csv(image, filename: str):
    if not filename.endswith('.csv'):
        filename = filename + '.csv'
    np.savetxt(filename, image, fmt='%1.0d', delimiter=',')

def reset():
    global image, image_copy, image_original, mask, mask_copy, mask_original, refPoint
    image = image_original.copy()
    image_copy = image_original.copy()
    mask = mask_original.copy()
    mask_copy = mask_original.copy()
    refPoint.clear()

image = cv2.imread(IMG_FILE_NAME)
image_copy = image.copy()   # Create a copy of the image for drawing purposes
image_original = image.copy()   # Save original image in case of reset

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', on_click)  # Assign the on_click function to the image
width, height = image.shape[:2]         # Get width and height of the image for mask

mask = np.zeros((width, height))        # Create mask
mask_copy = mask.copy()                 # Mask copy for drawing purposes
mask_original = mask.copy()             # Save original mask in case of reset

while True:
    cv2.imshow('Image', image)  # Show image
    cv2.imshow('mask', mask)    # Show mask
    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):             # If user presses r
        reset()
        lButtonDrag = False         # Indicate the user is not lButtonDrag
    elif key == 27:     # 27 represents escape key
        out = False
        break
    elif key == 13:
        out = True
        break

if out:
    write_to_csv(mask, OUTPUT_FILE_NAME)

cv2.destroyAllWindows()