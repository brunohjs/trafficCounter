from math import sqrt

class Vehicle:
    def __init__(self, frame, centroid):
        self.frame = frame
        self.no_frame = 0
        self.track = [centroid]
        self.current_pose = centroid

    def setCurrentPose(self, pose):
        self.track.append(pose)
        self.current_pose = pose

    def incrementNoFrame(self):
        self.no_frame += 1