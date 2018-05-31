from Vehicle import Vehicle
import numpy as np
import cv2
import sys
import time
import math

'''
def on_mouse(event, x, y, buttons, user_param):
    if event == cv2.EVENT_LBUTTONDOWN:
        polygon.append([x, y])
'''

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def getEuclidean(centroid, buffer):
    print(centroid)
    for points in buffer[:3]:
        for point in points:
            if centroid != point:
                d = math.sqrt((centroid[0]-point[0])**2 + (centroid[1]-point[1])**2)
                print(buffer.index(points), point, d)
    print('\n\n')

def detectVehicle(stats, centroids, frame, frame_id, buffer_frames, vehicle_counter):
    points = list()
    for i in range(len(stats)):
        stat = stats[i]
        area = stat[cv2.CC_STAT_AREA]
        centroid = (int(centroids[i][0]), int(centroids[i][1]))
        if area >= min_area:
            
            #vehicles.append(Vehicle(vehicle_id, frame, centroid))
            
            initial_point = (stat[cv2.CC_STAT_LEFT], stat[cv2.CC_STAT_TOP])
            initial_point_text = (initial_point[0], initial_point[1] - 5)
            final_point = (initial_point[0] + stat[cv2.CC_STAT_WIDTH], initial_point[1] + stat[cv2.CC_STAT_HEIGHT])
            #points.append((initial_point, final_point, area))
            
            if inSquare(road_points, centroid, 'bottom-up'):
                
                vehicle_counter += 1
                cv2.rectangle(frame, initial_point, final_point, (0, 0, 255), 1)
                cv2.circle(frame, centroid, 3, (0,255,255), -1)
                cv2.putText(
                    frame, 
                    classify(area, stat[cv2.CC_STAT_WIDTH], stat[cv2.CC_STAT_HEIGHT]),
                    initial_point_text, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1
                )
                if buffer_frames:
                    getEuclidean(centroid, buffer_frames)
                points.append(centroid)
    if points:
        buffer_frames = addFrame(points, buffer_frames, 10)
    return vehicle_counter, buffer_frames, frame


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

def findVehicle(points, max_distance=40):
    for vehicle in vehicles:
        for point in points:
            if distance(vehicle.current_pose, point) <= max_distance:
                #O ponto é um rastro do veículo
                pass

def addFrame(frame, buffer, max_size=10):
    if len(buffer) >= max_size:
        buffer.pop()
    buffer.insert(0, frame)
    return buffer


#def inCars(centroid):


VIDEO_SOURCE = sys.argv[1]
min_area = 500
vehicles = list()
vehicle_counter = 0
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

    vehicle_counter, buffer_frames, frame = detectVehicle(stats, centroids, frame, frame_id, buffer_frames, vehicle_counter)

    cv2.polylines(frame, [road_area], True, (0,255,0), 3)
    cv2.putText(frame,'COUNT: %r' %vehicle_counter, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow('Track', frame)
    cv2.imshow('Background', bkframe)
    time.sleep(2)

    if cv2.waitKey(100) == ord('q'):
            break