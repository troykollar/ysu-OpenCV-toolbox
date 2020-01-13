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

ref_points = []       # List for each corner of the rectangle
mouse_drag = False    # Says whether or not the user is currently dragging lbutton

NUM_MODES = 1
mode = 0

new_polygon = True

def on_click(event, x, y, flags, param):
    #Grab global variables
    global ref_points, mouse_drag, mask, mask_copy, image, image_copy, new_polygon, width, height
    if mode == 0:
        if event == cv2.EVENT_LBUTTONDOWN:  # Once click is started
            ref_points.append((x, y))         # Append first point of the rectangle
            mouse_drag = True                 # Indicate drawing has started

        if mouse_drag:               # while the user is dragging lButton
            if event == cv2.EVENT_LBUTTONUP:  # if user releases
                ref_points.append((x, y))          # append the second rectangle corner
                mask_copy = mask.copy()
                image_copy = image.copy()
                mouse_drag = False                # Indicate the user is no longer dragging lButton

                #Draw rectangle
                cv2.rectangle(image, ref_points[0], ref_points[1], (0, 255, 0), 1)
                cv2.rectangle(mask, ref_points[0], ref_points[1], (1), 0)

                ref_points.clear()    # Clear reference points so new rectangles can be drawn

            if event == cv2.EVENT_MOUSEMOVE:  # While user is mouse_drag, draw rectangle
                image = image_copy.copy()       # Revert to original image each mouse move, so rectangles don't overlap
                mask = mask_copy.copy()         # Revert to original mask each mouse move, so rectangles don't overlap

                #Draw rectangle
                cv2.rectangle(image, ref_points[0], (x, y), (0, 255, 0), 1)
                cv2.rectangle(mask, ref_points[0], (x, y), (1), -1)

    elif mode == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(ref_points) > 0:   # If a polygon is already started
                ref_points.append((x,y))  # Add point to polygon
                # draw lines on image and mask
                cv2.line(image, ref_points[-2], (x, y), (0, 255, 0), 1)
                cv2.line(mask, ref_points[-2], (x, y), (1), 1)
                # Set the copies to include lines on image
                image_copy = image.copy()
                mask_copy = mask.copy()
            elif new_polygon:   # If this click is the first point of a new polygon
                new_polygon = False     # Indicate a new polygon is no longer to be drawn
                ref_points.append((x,y))    # Add first point of polygon
            elif not new_polygon:    # Reset to new polygon after a double click
                new_polygon = True
        
        if len(ref_points) > 0:
            if event == cv2.EVENT_MOUSEMOVE:
                # Set image and mask to copy, so lines aren't drawn at every move
                image = image_copy.copy()
                mask = mask_copy.copy()
                # Draw lines
                cv2.line(image, ref_points[-1], (x, y), (0, 255, 0), 1)
                cv2.line(mask, ref_points[-1], (x, y), (1), 1)

        if len(ref_points) > 1:
            # At double click, attach current point to first point
            if event == cv2.EVENT_LBUTTONDBLCLK:
                cv2.line(image, ref_points[-1], ref_points[0], (0, 255, 0), 1)
                cv2.line(mask, ref_points[-1], ref_points[0], (1), 1)

                # Fill the polygon on the mask
                cv2.fillPoly(mask, [np.asarray(ref_points)], (1))

                # Set copies to include polygon
                image_copy = image.copy()
                mask_copy = mask.copy()

                # Clear the points so a new polygon can be drawn
                ref_points.clear()

def write_to_csv(image, filename: str):
    if not filename.endswith('.csv'):
        filename = filename + '.csv'
    np.savetxt(filename, image, fmt='%1.0d', delimiter=',')

def reset():
    global image, image_copy, image_original, mask, mask_copy, mask_original, ref_points
    image = image_original.copy()
    image_copy = image_original.copy()
    mask = mask_original.copy()
    mask_copy = mask_original.copy()
    ref_points.clear()

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
        mouse_drag = False         # Indicate the user is not mouse_drag
    if key == ord('m'):
        if mode == NUM_MODES:
            mode = 0
        else:
            mode += 1
    elif key == 27:     # 27 represents escape key
        out = False
        break
    elif key == 13:
        out = True
        break

if out:
    write_to_csv(mask, OUTPUT_FILE_NAME)

cv2.destroyAllWindows()