"""Generates and stores info for the user to draw and print mask on image"""
import cv2
import numpy as np

class ImageInfo:
    """Generates and stores info for the user to draw and print mask on image
    @param imgfile the filename of the image
    """
    MODES = ["Rectangle", "Polygon", "Above", "Below", "Right", "Left"]
    NUM_MODES = len(MODES)
    def __init__(self, imgfile):
        self._img = cv2.imread(imgfile)
        self._img_copy = self._img.copy()
        self._img_original = self._img.copy()
        self._height, self._width = self._img.shape[:2]
        self._mask = np.zeros((self.height, self.width))
        self._mask_copy = self._mask.copy()
        self._mask_original = self._mask.copy()
        self._new_polygon = False
        self._mouse_drag = False
        self._mouse_position = (0, 0)
        self._white_img = np.ones((180, 600))
        self._white_img_original = self._white_img.copy()
        self._ref_points = []
        self._mode = 0

    @property
    def height(self):
        """Getter for height variable"""
        return self._height

    @property
    def width(self):
        """Getter for width variable"""
        return self._width

    def reset(self):
        """Resets img and mask + copies to original state"""
        self.set_img_to_original()
        self.set_copy_to_original()
        self.clear_ref_points()
        self.mouse_drag = False

    @property
    def img_original(self):
        """Getter for the _img_original variable"""
        return self._img_original

    @property
    def mask_original(self):
        """Getter for _mask_original variable"""
        return self._mask_original

    def set_img_to_original(self):
        """Sets the img and mask to their original states"""
        self.img = self.img_original.copy()
        self.mask = self.mask_original.copy()

    def set_copy_to_original(self):
        """Sets the img_copy and mask_copy to their original states"""
        self.img_copy = self.img_original.copy()
        self.mask_copy = self.mask_original.copy()

    def fill_mask_polygon(self):
        """Fills the polygon that is drawn on the mask"""
        cv2.fillPoly(self._mask, [np.asarray(self.ref_points)], (1))

    def draw_lines(self, pt1, pt2):
        """Draws a line on both the image and the mask given endpoints"""
        cv2.line(self._img, pt1, pt2, (0, 255, 0), 1)
        cv2.line(self._mask, pt1, pt2, (1), 1)

    def clear_ref_points(self):
        """Clears the ref_points list"""
        self._ref_points.clear()

    def draw_rectangles(self, pt1, pt2):
        """Draws a rectangle on mask and image given top left and bottom right corner"""
        cv2.rectangle(self._img, pt1, pt2, (0, 255, 0), 1)
        cv2.rectangle(self._mask, pt1, pt2, (1), -1)

    @property
    def img(self):
        """Getter for _img variable"""
        return self._img

    @img.setter
    def img(self, new_img):
        """Setter for _img variable"""
        self._img = new_img

    @property
    def mask(self):
        """Getter for _mask variable"""
        return self._mask

    @mask.setter
    def mask(self, new_mask):
        """Setter for _mask variable"""
        self._mask = new_mask

    @property
    def img_copy(self):
        """Getter for _img_copy variable"""
        return self._img_copy

    @img_copy.setter
    def img_copy(self, new_img_copy):
        """Setter for _img_copy variable"""
        self._img_copy = new_img_copy

    @property
    def mask_copy(self):
        """Getter for _mask_copy variable"""
        return self._mask_copy

    @mask_copy.setter
    def mask_copy(self, new_mask_copy):
        """Setter for _mask_copy variable"""
        self._mask_copy = new_mask_copy

    def set_img_to_copy(self):
        """Sets the image and mask to their respective copies"""
        self._img = self.img_copy.copy()
        self._mask = self.mask_copy.copy()

    def set_copy_to_img(self):
        """Sets the image and mask copies to their respective images"""
        self._img_copy = self.img.copy()
        self._mask_copy = self.mask.copy()

    @property
    def mouse_drag(self):
        """Getter for mouse_drag variable"""
        return self._mouse_drag

    @mouse_drag.setter
    def mouse_drag(self, value):
        """Setter for mouse_drag variable"""
        if isinstance(value, (bool)):
            self._mouse_drag = value
        else:
            print(str(value) + " is not a valid mouse_drag value.")

    @property
    def new_polygon(self):
        """Getter for new_polygon variable"""
        return self._new_polygon

    @new_polygon.setter
    def new_polygon(self, value):
        """Setter for new_polygon variable"""
        if isinstance(value, (bool)):
            self._new_polygon = value
        else:
            print(str(value) + " is not a valid new_polygon value.")

    @property
    def ref_points(self):
        """Getter for ref_points list"""
        return self._ref_points

    def append_ref_points(self, new_point):
        """Appends new_point to the ref_points list. new_point must be a tuple (x, y)"""
        x, y = new_point
        self._ref_points = self._ref_points + [(x, y)]

    @property
    def mode(self):
        """Getter for mode variable"""
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        """Setter for mode variable"""
        if (new_mode >= 0) and (new_mode <= self.NUM_MODES):
            self._mode = new_mode
        else:
            print(str(new_mode) + "is not a valid mode.")

    @property
    def mouse_position(self):
        """Setter for mouse_position variable, returns a tuple (x, y)"""
        return self._mouse_position

    @mouse_position.setter
    def mouse_position(self, position):
        """Setter for mouse_position variable. position must be a tuple (x, y)"""
        x, y = position
        if x < 0:
            x = 0
        elif x > self._width:
            x = self._width
        if y < 0:
            y = 0
        elif y > self._height:
            y = self._height
        self._mouse_position = (x, y)

    @property
    def white_img(self):
        """Getter for white_img variable"""
        return self._white_img

    @property
    def white_img_original(self):
        """Getter for white_img_original variable"""
        return self._white_img_original

    def set_white_img_original(self):
        """Sets white_img to white_img_original"""
        self._white_img = self.white_img_original.copy()

    def write_position_to_white(self, position):
        """Resets white img to original,
        then writes mouse position to white_img. position must be a tuple (x, y)"""
        self.set_white_img_original()
        font = cv2.FONT_HERSHEY_DUPLEX
        fontsize = .75
        fontcolor = (0)
        modetext = self.MODES[self.mode]
        cv2.putText(self.white_img, "Mode: " + modetext, (5, 30),
                    font, fontsize, fontcolor)
        cv2.putText(self._white_img, "(" + str(position) + ")", (5, 60),
                    font, fontsize, fontcolor)
        cv2.putText(self._white_img, "Press 'M' to change mode.", (5, 90),
                    font, fontsize, fontcolor)
        cv2.putText(self._white_img, "Press 'Enter' to generate '.csv' file.", (5, 120),
                    font, fontsize, fontcolor)
        cv2.putText(self._white_img, "Press 'Esc' to exit.", (5, 150),
                    font, fontsize, fontcolor)
