from math import sqrt

class Vehicle:
    def __init__(self, vid, centroid):
        self.id = vid
        self.track = [centroid]
        self.current_pose = centroid

    def setCurrentPose(self, pose):
        self.track.append(pose)
        self.current_pose = pose

    def findTrack(self, points, min_distance=40):
        for point in points:
            d = sqrt((self.current_pose[0]-point[0])**2 + (self.current_pose[1]-point[1])**2)
            if d <= min_distance:
                pass
                #O ponto é um rastro do carro