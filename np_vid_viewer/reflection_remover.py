"""Utility to remove the heat reflection from an image"""
import os
import numpy as np
import cv2

class ReflectionRemover:
    def remove(img: np.ndarray, distance=0, min_value=174, max_temp_threshold=1900,
               zero_level_threshold=176, remove_lower=False, img_array=None, lower_bounds=None):
        """Set values above the hottest point to min_value to remove the reflection of heat.
        
        Args:
            img (np.ndarray) -- the img to remove the reflection from
            distance (int) -- the number of pixels above the hottest point to draw until (default 0)
            min_value (int) -- the minimum value read from the thermal camera (default 174)
            max_temp_threshold (int) --    the hotpoint must be greater than to continue removing reflections
                            this is useful to prevent removing parts of the image during cooling
            zero_level_threshold (int) -- lines that have an average value above zero_level_threshold will not be painted over
        """
        max_value = np.amax(img)
        max_value_location = np.where(img == max_value)

        if max_value > max_temp_threshold:
            remove_to = max_value_location[0][0]
            while np.mean(img[remove_to - distance]) > zero_level_threshold:
                if remove_to < 1:
                    print("Problem removing reflection.")
                    break
                else:
                    remove_to = remove_to - 1

            for i in range(0, remove_to - distance):
                img[i] = min_value

        if remove_lower:
            img_height = img.shape[0]
            for i in range(0, len(lower_bounds)):
                x = lower_bounds[i][0]
                y = lower_bounds[i][1]
                print(x,y)
                img[y:, x] = min_value
            