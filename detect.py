import Vehicle
import main
import cv2
from cartesian import distance

def detectVehicle(stats, centroids, frame, frame_id, buffer_frames, vehicles, road_points):
    points = list()
    for i in range(len(stats)):
        stat = stats[i]
        area = stat[cv2.CC_STAT_AREA]
        centroid = (int(centroids[i][0]), int(centroids[i][1]))

        if (area >= main.MIN_AREA) and inSquare(road_points, centroid, 'bottom-up'):
            if not vehicles:
                vehicles.append(Vehicle.Vehicle(len(vehicles), frame_id, centroid, stat))
            else:
                points.append([centroid, stat])
                cv2.circle(frame, centroid, 3, (127,127,255), -1)
            
    if buffer_frames:
        vehicles = findVehicles(vehicles, buffer_frames[0], frame_id, main.MAX_DISTANCE)
    print(points)
    if points:
        buffer_frames = addFrame(points, buffer_frames, 1)
    return buffer_frames, frame

def inSquare(road_area, point, way):
    high_y = road_area[1][1]
    low_y = road_area[0][1]
    high_x = int((road_area[2][0]+road_area[3][0])/2) + 5
    low_x = int((road_area[0][0]+road_area[1][0])/2) - 5
    if way == 'bottom-up':
        in_y = point[1] < high_y and point[1] > low_y
        in_x = point[0] < high_x and point[0] > low_x
        if in_x and in_y:
            return True
        else:
            return False

def findVehicles(vehicles, points, frame_id, max_distance=40):
    for vehicle in vehicles:
        found = False
        for point in points:
            if distance(vehicle.getCurrentPose(), point[0]) <= max_distance:
                vehicle.setCurrentPose(point[0], point[1], frame_id)
                points.remove(point)
                found = True
                break
        if not found:
            vehicle.incrementNoFrame()
    if points:
        for point in points:
            vehicles.append(Vehicle.Vehicle(len(vehicles), frame_id, point[0], point[1]))
    return vehicles

def addFrame(frame, buffer, max_size=10):
    if len(buffer) >= max_size:
        buffer.pop()
    buffer.insert(0, frame)
    return buffer