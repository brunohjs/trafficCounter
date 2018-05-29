import numpy as np
import cv2

VIDEO_SOURCE = 'video.mp4'

capture = cv2.VideoCapture(VIDEO_SOURCE) 
backsub = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame = capture.read()
    bkframe = backsub.apply(frame, None, 0.01)
    bkframe = cv2.medianBlur(bkframe, 5)
    bkframe = cv2.blur(bkframe, (5,5))

    pts = np.array([ [110,165], [19,233], [202,233], [217, 165] ], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(frame, [pts], True, (0,255,0), 2)

    #cv2.putText(frame,'COUNT: %r' %i, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    #cv2.imshow("Track", frame)
    cv2.imshow('BK', bkframe)

    key = cv2.waitKey(100)
    if key == ord('q'):
            break