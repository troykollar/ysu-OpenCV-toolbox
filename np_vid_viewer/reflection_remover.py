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
            img_width = img.shape[1]
            top_level = 0

            for y in range(0, img_height):
                for x in range(0, img_width):
                    if img[y,x] > zero_level_threshold:
                        values = []
                        #Make a list of non "zero" values in column
                        for i in range(y, img_height - 1):
                            if img[i, x] > zero_level_threshold:
                                values.append(img[i, x])
                            else:
                                break
                        if len(values) > 3:     # If there is enough values for a reflection
                            max_in_list = max(values)
                            vals_after_max = values[values.index(max_in_list) : len(values)]
                            print(min(vals_after_max))
                            if min(vals_after_max) <= zero_level_threshold + 30:
                                end_of_part = y + vals_after_max.index(min(vals_after_max))
                                img[end_of_part:, x] = min_value
                                print(x, "End of part:", end_of_part)

            """
            for i in range(0, img_height):
                if np.mean(img[i]) > zero_level_threshold:
                    top_level = i
                    break
            for x in range(0, img_width):   #Find top of part
                if img[top_level, x] > min_value:
                    values = []
                    #Make a list of non "zero" values in column
                    for y in range(top_level, img_height - 1):
                        if img[y, x] > zero_level_threshold:
                            values.append(img[y, x])
                        else:
                            print(x, y)
                            img[y:, x] = min_value
                            break

                    if len(values) > 3:     # If there is enough values for a reflection
                        max_in_list = max(values)
                        vals_after_max = values[values.index(max_in_list) : len(values)]
                        end_of_part = top_level + vals_after_max.index(min(vals_after_max))
                        print(x,y)
                        print("End of part:", end_of_part)
                        if y < end_of_part:
                            img[y:, x] = min_value
                        else:
                            img[end_of_part:, x] = min_value
                        values.clear()"""
