import cartesian
import main
import numpy as np
import cv2

class Vehicle:
    def __init__(self, vid, frame, centroid, stat):
        self.vid = vid
        self.frame = frame
        self.no_frame = 0
        self.track = [centroid]
        self.current_pose = centroid
        self.stat = stat
        self.hide = False

    def setCurrentPose(self, pose, stat, frame):
        self.track.insert(0, pose)
        self.current_pose = pose
        self.stat = stat
        self.frame = frame
        self.no_frame = 0
    
    def getCurrentPose(self):
        return self.current_pose

    def getArea(self):
        return self.stat[cv2.CC_STAT_AREA]

    def incrementNoFrame(self):
        self.no_frame += 1
        if self.no_frame == 8:
            self.hide = True

    def show(self):
        print('-----------------')
        print('vid: ', self.vid)
        print('frame: ', self.frame)
        print('track: ', self.track)
        print('pose: ', self.current_pose)
        print('------------------\n')

    def drawTrack(self, frame):
        track = np.array(self.track, np.int32)
        track = track.reshape((-1,1,2))
        cv2.polylines(frame, [track], False, (255, 255, 0), 2)

    def drawVehicle(self, frame):
        initial_point = (self.stat[cv2.CC_STAT_LEFT], self.stat[cv2.CC_STAT_TOP])
        final_point = (initial_point[0] + self.stat[cv2.CC_STAT_WIDTH], initial_point[1] + self.stat[cv2.CC_STAT_HEIGHT])
        initial_point_text = (initial_point[0], initial_point[1] - 5)
        cv2.rectangle(frame, initial_point, final_point, (0, 0, 255), 1)
        cv2.circle(frame, self.current_pose, 3, (0,255,255), -1)
        cv2.putText(
            frame, 
            self.classify(self.stat[cv2.CC_STAT_WIDTH], self.stat[cv2.CC_STAT_HEIGHT])+' '+str(self.vid),
            initial_point_text, 
            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1
        )

    def classify(self, width, height):
        area = self.getArea()
        #car = (area <= MIN_AREA+(MIN_AREA*1.0)) and (area > MIN_AREA)
        truck = area > main.MIN_AREA*4
        if truck:
            return 'truck'
        else:
            return 'car/van'

    def diffAngle(self):
        points = self.track[-3:]
        v1 = cartesian.vector(points[0], points[1])
        v2 = cartesian.vector(points[1], points[2])
        v3 = cartesian.vector(points[0], points[2])
        angle0 = cartesian.angleVectors(v1, v2)
        angle0 = cartesian.angleVectors(v1, v3)

    def isHide(self):
        return self.hide