from math import sqrt
import numpy as np
import cv2

class Vehicle:
    def __init__(self, frame, centroid):
        self.frame = frame
        self.no_frame = 0
        self.track = [centroid]
        self.current_pose = centroid

    def setCurrentPose(self, pose):
        self.track.insert(0, pose)
        self.current_pose = pose
        self.no_frame = 0

    def incrementNoFrame(self):
        self.no_frame += 1

    def show(self):
        print('-----------------')
        print('frame: ', self.frame)
        print('track: ', self.track)
        print('pose: ', self.current_pose)
        print('------------------\n')

    def drawTrack(self, frame):
        track = np.array(self.track, np.int32)
        track = track.reshape((-1,1,2))
        cv2.polylines(frame, [track], False, (255, 255, 0), 2)
