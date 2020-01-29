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
        self._timestamps = np.load(tc_times, allow_pickle=True)
        if melt_pool_data is not None:
            self._melt_pool_data = np.load(melt_pool_data, allow_pickle=True)
        else:
            self._melt_pool_data = None

        self._mp_data_index = 0
        self.match_vid_to_meltpool()

    def match_vid_to_meltpool(self):
        self._matched_array = []
        for i in range(0, self.array.shape[0]):
            if self.mp_data_index + 1 < self.melt_pool_data.shape[0]:
                if self.timestamps[i] >= self.melt_pool_data[self.mp_data_index + 1][0]:
                    self.mp_data_index = self.mp_data_index + 1
            self._matched_array.append([i, self.timestamps[i], self.melt_pool_data[self.mp_data_index][0],
                                        self.melt_pool_data[self.mp_data_index][1],
                                        self.melt_pool_data[self.mp_data_index][2],
                                        self.melt_pool_data[self.mp_data_index][3],
                                        self.melt_pool_data[self.mp_data_index][4]])

    @property
    def num_frames(self):
        return self._num_frames

    def video_timestamp(self, frame):
        return self.matched_array[frame][1]

    def mp_timestamp(self, frame):
        return self.matched_array[frame][2]

    def mp_x(self, frame):
        return self.matched_array[frame][3]

    def mp_y(self, frame):
        return self.matched_array[frame][4]

    def mp_z(self, frame):
        return self.matched_array[frame][5]

    def mp_area(self, frame):
        return self.matched_array[frame][6]

    @property
    def matched_array(self):
        return self._matched_array

    @property
    def mp_data_index(self):
        return self._mp_data_index

    @mp_data_index.setter
    def mp_data_index(self, value: int):
        if value < 0:
            self._mp_data_index = 0
        elif value > self._melt_pool_data.shape[0]:
            self._mp_data_index = self._melt_pool_data.shape[:0][0]
        else:
            self._mp_data_index = value

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

    def print_info(self, frame):
        print("Frame: " + str(frame),
              "| TC time: " + str(self.mp_timestamp(frame).replace(microsecond = 0)),
              "| MP time: " + str(self.mp_timestamp(frame).replace(microsecond = 0)),
              "| MP X: " + str(self.mp_x(frame)), 
              "| MP Y: " + str(self.mp_y(frame)), 
              "| MP Z: " + str(self.mp_z(frame)),
              "| MP Area: " + str(self.mp_area(frame)))

    def update_image(self, frame: int):
        img = self.array[frame]
        font = cv2.FONT_HERSHEY_DUPLEX
        normalized_img = cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        normalized_img = cv2.applyColorMap(normalized_img, cv2.COLORMAP_INFERNO)

        img_height = normalized_img.shape[:1][0]
        font_size = img_height/480
        font_color = (255, 255, 255)
        normalized_img = cv2.putText(normalized_img, "X: " + str(self.mp_x(frame)),
                                     (50, int((1/16)*img_height)), font, font_size, font_color)
        normalized_img = cv2.putText(normalized_img, "Y: " + str(self.mp_y(frame)),
                                     (50, int((2/16)*img_height)), font, font_size, font_color)
        normalized_img = cv2.putText(normalized_img, "Z: " + str(self.mp_z(frame)), 
                                     (50, int((3/16)*img_height)), font, font_size, font_color)
        normalized_img = cv2.putText(normalized_img, "Area: " + str(self.mp_area(frame)),
                                     (50, int((4/16)*img_height)), font, font_size, font_color)
        self.print_info(frame)
        cv2.imshow(self.window_name, normalized_img)

    def play_video(self, speed=1):
        self.speed = speed
        pause = False
        frame = 0
        data_list = []
        while True:
            key = cv2.waitKey(self.speed)
            if not pause:
                self.update_image(frame)
                frame = frame + 1
            elif pause:
                if key == ord('s'):
                    np.savetxt('tc_temps-' + str(i + 1) + ".csv", img, fmt='%d', delimiter=",")
                elif key == ord('l'):
                    frame = frame + 10
                    self.update_image(frame)
                elif key == ord('j'):
                    if frame > 10:
                        frame = frame - 10
                    else:
                        frame = 0
                    self.update_image(frame)
                    
            if key == ord('q'):
                break
            elif key == ord('k'):
                pause = not pause
            elif  frame >= self.num_frames:
                break
        cv2.destroyAllWindows