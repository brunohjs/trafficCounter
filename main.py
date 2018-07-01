
import detect
import cartesian

import numpy as np
import cv2
import sys
import time

VIDEO_SOURCE = sys.argv[1]
MIN_AREA = 400
MAX_DISTANCE = 30

MEDIA_BLUR = 9
BLUR = 7

'Função de aprendizado do background'
def learnSub(backsub, video_source, n_frames=50):
    capture = cv2.VideoCapture(VIDEO_SOURCE)
    while capture.isOpened():
        ret, frame = capture.read()
        bkframe = backsub.apply(frame, None, 0.01)
        if capture.get(1) == n_frames:
            capture.release()
            break
    return bkframe
    
'Logger do buffer'
def logger(buffer, frame_id, count=None):
    print('Count: ', count)
    print('Frame: ', frame_id)
    for v in buffer:
        print(v, cartesian.distance(v['centroid'], (0,0)))
    print('\n')

'Função principal'
def main():
    buffer_vehicles = list()
    vehicle_counter = 0

    backsub = cv2.bgsegm.createBackgroundSubtractorMOG(nmixtures=3)
    bkframe = learnSub(backsub, VIDEO_SOURCE, 100)
    capture = cv2.VideoCapture(VIDEO_SOURCE)

    if VIDEO_SOURCE == 'video.mp4':
        road_line = [(60, 180), (350, 180)]
    elif VIDEO_SOURCE == 'video3.mp4':
        road_line = [(0, 220), (350, 220)]
    elif VIDEO_SOURCE == 'video3.mp4':
        road_line = [(0, 220), (350, 220)]
    elif VIDEO_SOURCE == 'video4.mp4':
        road_line = [(0, 200), (350, 200)]

    cv2.namedWindow('Background')
    cv2.moveWindow('Background', 400, 0)
    cv2.namedWindow('Track')

    while True:
        try:
            frame_id = int(capture.get(1))
            ret, frame = capture.read()
            
            bkframe = backsub.apply(frame, None, 0.01)
            bkframe = cv2.medianBlur(bkframe, MEDIA_BLUR)
            bkframe = cv2.blur(bkframe, (BLUR,BLUR))

            num, labels, stats, centroids = cv2.connectedComponentsWithStats(bkframe, ltype=cv2.CV_16U)
            counter, buffer_vehicles, frame = detect.detectVehicle(
                stats[1:], 
                centroids, 
                frame, 
                frame_id, 
                buffer_vehicles,
                road_line)
            
            vehicle_counter += counter
            logger(buffer_vehicles, frame_id, vehicle_counter)

            cv2.line(frame, road_line[0], road_line[1], (0,255,0), 3)
            cv2.putText(frame,'COUNT: %r' %vehicle_counter, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            #cv2.imwrite('img/drw2/frm'+str(frame_id)+'.png', frame)
            
            cv2.imshow('Track', frame)
            cv2.imshow('Background', bkframe)
            #time.sleep(0.1)

            if cv2.waitKey(100) == ord('q') or not capture.isOpened():
                break
        except:
            break

    counter, buffer_vehicles = detect.countVehicles(buffer_vehicles, frame_id, MAX_DISTANCE, final=True)
    vehicle_counter += counter
    logger(buffer_vehicles, frame_id, vehicle_counter)

if __name__ == '__main__':
    main()