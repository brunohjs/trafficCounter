
import Vehicle
import detect

import numpy as np
import cv2
import sys
import time

"""
def on_mouse(event, x, y, buttons, user_param):
    if event == cv2.EVENT_LBUTTONDOWN:
        polygon.append([x, y])
"""   

#def inCars(centroid):

VIDEO_SOURCE = sys.argv[1]
MIN_AREA = 500

def main():
    vehicles = list()
    buffer_frames = list()

    capture = cv2.VideoCapture(VIDEO_SOURCE)
    backsub = cv2.bgsegm.createBackgroundSubtractorMOG()

    #cv2.setMouseCallback("Draw Polygon", on_mouse)

    road_points = [[90,180], [5,244], [202,244], [214,180]]     #video.mp4
    road_area = np.array(road_points, np.int32)
    road_area = road_area.reshape((-1,1,2))

    cv2.namedWindow('Background')
    cv2.moveWindow('Background', 400, 0)
    cv2.namedWindow('Track')

    while capture.isOpened():
        frame_id = int(capture.get(1))
        ret, frame = capture.read()
        
        bkframe = backsub.apply(frame, None, 0.01)
        bkframe = cv2.medianBlur(bkframe, 7)
        bkframe = cv2.blur(bkframe, (7,7))

        num, labels, stats, centroids = cv2.connectedComponentsWithStats(bkframe, ltype=cv2.CV_16U)

        buffer_frames, frame = detect.detectVehicle(stats, centroids, frame, frame_id, buffer_frames, vehicles, road_points)
        for vehicle in vehicles:
            if not vehicle.isHide():
                vehicle.show()
                vehicle.drawVehicle(frame)
                vehicle.drawTrack(frame)

        cv2.polylines(frame, [road_area], True, (0,255,0), 3)
        #cv2.putText(frame,'COUNT: %r' %vehicle_counter, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow('Track', frame)
        cv2.imshow('Background', bkframe)
        #time.sleep(0.5)

        if cv2.waitKey(100) == ord('q'):
                break


if __name__ == '__main__':
    main()