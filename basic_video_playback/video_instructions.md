# Reading and displaying a video in OpenCV

Reading and displaying video is done using the `VideoCapture()` function.

```
import cv2

#store the video file as a video capture object
cap = cv2.VideoCapture('Megamind.avi')

#If there is an error opening the video, output an error
if (cap.isOpened() == False):
    print("Error opening video file")

#while loop to read video until it is completed
while(cap.isOpened()):
    #capture each frame of video
    ret, frame = cap.read()
    if ret == True:     #if frame is successfully read
        cv2.imshow('Frame',frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break  
    else:               #frame is not read
        break

cap.release()
cv2.destroyAllWindows
```

We start by storing the video as an object with the `VideoCapture()` function. As shown in `cap = cv2.VideoCapture('Megamind.avi')`. `VideoCapture()` can also be used to capture live video by using a 0 or a 1 as the argument (0 meaning the first camera, 1 meaning the second camera).

Next a while loop is used to read each individual frame. `cap.read()` is used to read each frame of the video capture object. It returns a `retval` and `frame` object. `retval` is a boolean that indicates whether or not the frame was read successfully, and `frame` is the actual image that is used for each frame.

After determining `ret` is true, we can display each frame using `imshow` the same way we would with still images.

The following lines, determine if the 'q' key has been pressed, and if so, breaks from the loop.
```
if cv2.waitKey(25) & 0xFF == ord('q'):
            break  
```
Now it is neccesary to release the video capture object with `cap.release()`, and destroy the windows with `destroyAllWindows`.