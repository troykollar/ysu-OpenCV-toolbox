# Working with Videos

Working with videos in OpenCV is very similar to working with images. The difference being that you work with each frame as an individual image, and playback all of those frames. In [`videoTracking.py`](videoTracking.py) we'll do hsv object tracking like we did with images in [`hsv_object_detection`](../hsv_object_detection).

The first thing we'll do is capture the video file using `cv2.VideoCapture()`, and set a boolean value that we can use to pause the video if needed.

```
cap = cv2.VideoCapture('box.mp4')
playVideo = True
```



Next we create a loop to see when the ensure commands are run on each frame. If `playVideo` is true, meaning we haven't paused the video, run `cap.read()`. This function returns 2 values. A boolean return value, which is true if a frame was successfully read, and false otherwise.  And the image of the frame itself.

```
while (cap.isOpened()):
    #If we haven't quit the video, read the next frame
    if playVideo == True:
        ret, frame = cap.read()
```

Now we perform our commands on the frame if it was read successfully. We've already determined our lower and upper hsv bounds using trackbars in a previous example.

```
if ret == True:
    lowerBound = np.array([30, 0, 0])
    upperBound = np.array([120, 255, 255])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        #get hsv version of video
    mask = cv2.inRange(hsv, lowerBound, upperBound)     #get mask
    result = cv2.bitwise_and(frame,frame, mask=mask)    #bitwise_and with mask to get resulting image
    edged = cv2.Canny(result,30,150)                    #Calculate edges

    #Calculate contours to show edges of our tracked image
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #Draw the contours onto the frame
    cv2.drawContours(frame, contours, -1, (0,255,0),3)

    cv2.imshow('Mask', mask)
    cv2.imshow('Contours', frame)
```

Before ending the loop, we need to determine if we should pause the video our quit the program.

```
key = cv2.waitKey(5)
if cv2.waitKey(10) & 0xFF == ord('p'):
    playVideo = not playVideo

if cv2.waitKey(10) & 0xFF == ord('q'):
    break
```

Lastly, the video capture variable needs to be released and all windows destroyed.

```
cap.release()
cv2.destroyAllWindows()
```