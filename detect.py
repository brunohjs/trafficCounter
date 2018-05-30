import numpy as np
import cv2
import sys

def detectVehicle(stat, centroid):
    area = stat[cv2.CC_STAT_AREA]
    initial_point = (stat[cv2.CC_STAT_LEFT], stat[cv2.CC_STAT_TOP])
    initial_point_text = (initial_point[0], initial_point[1] - 5)
    final_point = (initial_point[0] + stat[cv2.CC_STAT_WIDTH], initial_point[1] + stat[cv2.CC_STAT_HEIGHT])
    #candidates.append((initial_point, final_point, area))
    
    if inSquare(road_points, centroid, 'bottom-up'):
        cv2.rectangle(frame, initial_point, final_point, (0, 0, 255), 1)
        cv2.circle(frame, centroid, 3, (0,255,255), -1)
        cv2.putText(
            frame, 
            classify(area, stat[cv2.CC_STAT_WIDTH], stat[cv2.CC_STAT_HEIGHT]),
            initial_point_text, 
            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1
        )


def classify(area, width, height):
    car = (area <= min_area+(min_area*1.0)) and (area > min_area)
    truck = area > min_area*4
    if car:
        return 'car'
    elif truck:
        return 'truck'
    else:
        return 'other'


def inSquare(area, point, way):
    high_y = area[1][1]
    low_y = area[0][1]
    high_x = int((area[2][0]+area[3][0])/2) + 5
    low_x = int((area[0][0]+area[1][0])/2) - 5
    if way == 'bottom-up':
        in_y = point[1] < high_y and point[1] > low_y
        in_x = point[0] < high_x and point[0] > low_x
        if in_x and in_y:
            return True
        else:
            return False



VIDEO_SOURCE = sys.argv[1]

capture = cv2.VideoCapture(VIDEO_SOURCE) 
backsub = cv2.bgsegm.createBackgroundSubtractorMOG()

road_points = [[90,180], [5,244], [202,244], [214,180]]
road_area = np.array(road_points, np.int32)
road_area = road_area.reshape((-1,1,2))

cv2.namedWindow("BK")
cv2.moveWindow("BK", 400, 0)

while True:
    ret, frame = capture.read()

    bkframe = backsub.apply(frame, None, 0.01)
    bkframe = cv2.medianBlur(bkframe, 9)
    bkframe = cv2.blur(bkframe, (7,7))
    cv2.polylines(frame, [road_area], True, (0,255,0), 3)

    num, labels, stats, centroids = cv2.connectedComponentsWithStats(bkframe, ltype=cv2.CV_16U)
    min_area = 500
    candidates = list()

    for i in range(len(stats)):
        stat = stats[i]
        centroid = (int(centroids[i][0]), int(centroids[i][1]))

        '''
        if classify(area, stat[cv2.CC_STAT_WIDTH], stat[cv2.CC_STAT_HEIGHT]) != 'truck':
            print((area, stat[cv2.CC_STAT_WIDTH], stat[cv2.CC_STAT_HEIGHT]), classify(area, stat[cv2.CC_STAT_WIDTH], stat[cv2.CC_STAT_HEIGHT]))
        '''

        if stat[cv2.CC_STAT_AREA] >= min_area:
            detectVehicle(stat, centroid)

    #cv2.putText(frame,'COUNT: %r' %i, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Track", frame)
    
    cv2.imshow('BK', bkframe)

    key = cv2.waitKey(100)
    if key == ord('q'):
            break