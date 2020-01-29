import cv2
import numpy as np
import datetime

class NpVidViewer:
    def __init__(self, filename: str, window_name="Video", melt_pool_data=None, tc_times=None):
        self._array = np.load(filename, mmap_mode='r', allow_pickle=True)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 640, 480)
        self._speed = 1
        self._window_name = window_name
        self._num_frames = self.array.shape[0]
        if tc_times is not None:
            self._timestamps = np.load(tc_times, allow_pickle=True)
        else:
            self._timestamps = None
        if melt_pool_data is not None:
            self._melt_pool_data = np.load(melt_pool_data, allow_pickle=True)
        else:
            self._melt_pool_data = None

    @property
    def melt_pool_data(self):
        return self._melt_pool_data

    @property
    def num_frames(self):
        return self._num_frames

    @property
    def window_name(self):
        return self._window_name

    @property
    def array(self):
        return self._array

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed):
        if new_speed < 1:
            self._speed = 1
        elif new_speed > 1000:
            self._speed = 1000
        else:
            self._speed = new_speed

    @property
    def timestamps(self):
        return self._timestamps

    def update_image(self, frame: int, mp_data_index: int, current_time_stamp):
        img = self.array[frame]
        font = cv2.FONT_HERSHEY_DUPLEX
        normalized_img = img.copy()
        normalized_img = cv2.normalize(normalized_img, normalized_img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        normalized_img = cv2.applyColorMap(normalized_img, cv2.COLORMAP_INFERNO)
        img_height = normalized_img.shape[:1][0]
        font_size = img_height/480
        font_color = (255, 255, 255)
        normalized_img = cv2.putText(normalized_img, "X: " + 
                                        str(self.melt_pool_data[mp_data_index][1]),
                                        (50, int(img_height/16)), font, font_size, font_color)
        normalized_img = cv2.putText(normalized_img, "Y: " + 
                                        str(self.melt_pool_data[mp_data_index][2]),
                                        (50,int((2/16)*img_height)), font, font_size, font_color)
        normalized_img = cv2.putText(normalized_img, "Z: " + 
                                        str(self.melt_pool_data[mp_data_index][3]), 
                                        (50,int((3/16)*img_height)), font, font_size, font_color)
        normalized_img = cv2.putText(normalized_img, "Area: " + 
                                        str(self.melt_pool_data[mp_data_index][4]),
                                        (50,int((4/16)*img_height)), font, font_size, font_color)
        cv2.imshow(self.window_name, normalized_img)
        print("Frame: " + str(frame), "| TC time: " + str(current_time_stamp.replace(microsecond=0)),
                "| MP time: " + str(self.melt_pool_data[mp_data_index][0].replace(microsecond=0)),
                "| MP X: " + str(self.melt_pool_data[mp_data_index][1]), 
                "| MP Y: " + str(self.melt_pool_data[mp_data_index][2]), 
                "| MP Z: " + str(self.melt_pool_data[mp_data_index][3]),
                "| MP Area: " + str(self.melt_pool_data[mp_data_index][4]))

    def play_video(self, speed=1):
        self.speed = speed
        pause = False
        frame = 0
        mp_data_index = 0
        data_list = []
        while True:
            key = cv2.waitKey(self.speed)
            if self.timestamps is not None:
                current_time_stamp = self.timestamps[frame]
            else:
                current_time_stamp = None
            if current_time_stamp.replace(microsecond=0) >= self.melt_pool_data[mp_data_index + 1][0].replace(microsecond=0):
                mp_data_index = mp_data_index + 1
            if not pause:
                self.update_image(frame, mp_data_index, current_time_stamp)
                frame = frame + 1
            elif pause:
                if key == ord('s'):
                    np.savetxt('tc_temps-' + str(i + 1) + ".csv", img, fmt='%d', delimiter=",")
                elif key == ord('l'):
                    frame = frame + 10
                    self.update_image(frame, mp_data_index, current_time_stamp)
                elif key == ord('j'):
                    if frame > 10:
                        frame = frame - 10
                    else:
                        frame = 0
                    self.update_image(frame, mp_data_index, current_time_stamp)
            if key == ord('q'):
                break
            elif key == ord('k'):
                pause = not pause
            elif  frame >= self.num_frames:
                break
        cv2.destroyAllWindows