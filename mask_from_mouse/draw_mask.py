"""Allows the user to draw masks on the image and write mask to csv file"""
import argparse
import cv2
import numpy as np
from image_info import ImageInfo

PARSER = argparse.ArgumentParser()
PARSER.add_argument("ImgFile", type=str,
                    help="The filename (and location if not in the same folder) of the image.")
PARSER.add_argument("OutFile", type=str,
                    help="The desired name of the csv output file (including .csv extension)")

ARGS = PARSER.parse_args()

IMG_FILE_NAME = ARGS.ImgFile
OUTPUT_FILE_NAME = ARGS.OutFile

img_info = ImageInfo(IMG_FILE_NAME)     # img_info object generates and stores relevant info

def on_click(event, x, y, flags, param):
    """Mouse callback function for the image window"""
    img_info.mouse_position = (x, y)
    if img_info.mode == 0:
        if event == cv2.EVENT_LBUTTONDOWN:  # Once click is started
            img_info.append_ref_points((x, y))         # Append first point of the rectangle
            img_info.mouse_drag = True                 # Indicate drawing has started

        if img_info.mouse_drag:               # while the user is dragging lButton
            if event == cv2.EVENT_LBUTTONUP:  # if user releases
                img_info.append_ref_points((x, y))  # append the second rectangle corner
                img_info.set_copy_to_img()
                img_info.mouse_drag = False     # Indicate the user is no longer dragging lButton

                #Draw rectangle
                img_info.draw_rectangles(img_info.ref_points[0], img_info.ref_points[1])
                img_info.clear_ref_points()   # Clear ref pts so new rectangles can be drawn

            if event == cv2.EVENT_MOUSEMOVE:  # While user is mouse_drag, draw rectangle
                # Revert to copy each mouse move to prevent rectangle overlap
                img_info.set_img_to_copy()
                img_info.draw_rectangles(img_info.ref_points[0], (x, y))    #Draw rectangle

    elif img_info.mode == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(img_info.ref_points) > 0:   # If a polygon is already started
                img_info.append_ref_points((x, y))  # Add point to polygon
                # draw lines on image and mask
                img_info.draw_lines(img_info.ref_points[-2], (x, y))
                # Set the copies to include lines on image
                img_info.set_copy_to_img()
            elif img_info.new_polygon:   # If this click is the first point of a new polygon
                img_info.new_polygon = False     # Indicate a new polygon is no longer to be drawn
                img_info.append_ref_points((x, y))  # Add first point of polygon
            elif not img_info.new_polygon:    # Reset to new polygon after a double click
                img_info.new_polygon = True
        if len(img_info.ref_points) > 0:
            if event == cv2.EVENT_MOUSEMOVE:
                img_info.set_img_to_copy()  # Revert image copy to prevent line overlapping
                img_info.draw_lines(img_info.ref_points[-1], (x, y)) # Draw lines

        if len(img_info.ref_points) > 1:
            if event == cv2.EVENT_LBUTTONDBLCLK:
                # At double click, attach current point to first point
                img_info.draw_lines(img_info.ref_points[-1], img_info.ref_points[0])
                img_info.fill_mask_polygon()    # Fill the polygon on the mask
                img_info.set_copy_to_img()  # Set copies to include polygon
                img_info.clear_ref_points() # Clear the points so a new polygon can be drawn
    elif img_info.mode == 2:    # Above mode
        if event == cv2.EVENT_LBUTTONDOWN:
            img_info.draw_rectangles((0, y), (img_info.width, 0))
            img_info.set_copy_to_img()
    elif img_info.mode == 3:    # Below mode
        if event == cv2.EVENT_LBUTTONDOWN:
            img_info.draw_rectangles((0, y), (img_info.width, img_info.height))
            img_info.set_copy_to_img()
    elif img_info.mode == 4:    # Right mode
        if event == cv2.EVENT_LBUTTONDOWN:
            img_info.draw_rectangles((x, 0), (img_info.width, img_info.height))
            img_info.set_copy_to_img()
    elif img_info.mode == 5:    # Left mode
        if event == cv2.EVENT_LBUTTONDOWN:
            img_info.draw_rectangles((x, 0), (0, img_info.height))
            img_info.set_copy_to_img()

def write_to_csv(image, filename: str):
    """Writes the numpy array of the image to a csv file"""
    if not filename.endswith('.csv'):
        filename = filename + '.csv'
    np.savetxt(filename, image, fmt='%1.0d', delimiter=',')

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', on_click)  # Assign the on_click function to the image
cv2.namedWindow('Mouse Position')
cv2.imshow('Image', img_info.img)  # Show image
cv2.moveWindow('Image', 20, 100)
cv2.imshow('mask', img_info.mask)    # Show mask
cv2.moveWindow('mask', img_info.width + 50, 110)
cv2.imshow('Mouse Position', img_info.white_img)
cv2.moveWindow('Mouse Position', 20, img_info.height + 175)

while cv2.getWindowProperty('Image',0) >= 0:
    img_info.write_position_to_white(img_info.mouse_position)
    cv2.imshow('Image', img_info.img)  # Show image
    cv2.imshow('mask', img_info.mask)    # Show mask
    cv2.imshow('Mouse Position', img_info.white_img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):             # If user presses r
        img_info.reset()
    if key == ord('m'):
        if img_info.mode == img_info.NUM_MODES - 1:
            img_info.mode = 0
        else:
            img_info.mode += 1
    elif (key == 27):     # 27 represents escape key
        out = False
        break
    elif key == 13:
        out = True
        break

if out:
    write_to_csv(img_info.mask, OUTPUT_FILE_NAME)

cv2.destroyAllWindows()
