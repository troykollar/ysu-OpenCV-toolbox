import cv2

#store the video file as a video capture object
cap = cv2.VideoCapture('Megamind.avi')

#If there is an error opening the video, output an error
if (cap.isOpened() == False):
    print("Error opening video file")

#whiel loop to read video until it is completed
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