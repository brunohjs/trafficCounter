
import main
import cv2
from cartesian import distance

def drawArea(frame, stat, centroid, area, color=(0,255,255)):
    #final_point = (initial_point[0] + stat[cv2.CC_STAT_WIDTH], initial_point[1] + stat[cv2.CC_STAT_HEIGHT])
    #initial_point_text = (initial_point[0], initial_point[1] - 5)
    #cv2.rectangle(frame, initial_point, final_point, (0, 0, 255), 1)
    cv2.circle(frame, centroid, 3, color, -1)
    '''
    cv2.putText(
        frame, 
        classify(area), 
        initial_point_text, 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.3, 
        (0, 0, 255), 
        1
    )
    '''

def detectVehicle(stats, centroids, frame, frame_id, buffer, road_line):
    n_vehicles = 0
    for i in range(len(stats)):
        stat = stats[i]
        area = stat[cv2.CC_STAT_AREA]
        centroid = (int(centroids[i][0]), int(centroids[i][1]))
        if area >= main.MIN_AREA:
            drawArea(frame, stat, centroid, area, (0,255,255))
            if inLine(road_line, centroid):
                drawArea(frame, stat, centroid, area, (255,0,0))
                buffer.append({
                    'id': frame_id,
                    'centroid' : centroid,
                    'area' : area 
                })
        
    if buffer:
        n_vehicles, buffer = countVehicles(buffer, frame_id, main.MAX_DISTANCE)
    #n_vehicles = 0

    return n_vehicles, buffer, frame

def inLine(road_line, point, sensibility=10):
    in_x = road_line[0][0] < point[0] < road_line[1][0] 
    in_y = (road_line[0][1]-sensibility) <= point[1] <= (road_line[1][1]+sensibility)
    if in_x and in_y:
        return True
    else:
        return False

def countVehicles(buffer, current_frame_id, max_distance=30, final=False):
    counter = 0
    i = 0
    while i < len(buffer)-1:
        j = i+1
        while j <= len(buffer)-1:
            near = distance(buffer[i]['centroid'], buffer[j]['centroid']) <= max_distance
            same = abs(buffer[i]['id'] - buffer[j]['id']) <= 5
            #in_this_frame = max(buffer[i]['id'], buffer[i+1]['id']) == current_frame_id
            #print(buffer[i], buffer[j], near, same)
            if near and same:
                del(buffer[i])
                break
            else:
                j += 1
        i += 1

    for vehicle in buffer:
        if abs(vehicle['id'] - current_frame_id) >= 15:
            counter += 1 
            buffer.remove(vehicle)
    if final:
        counter += len(buffer)
        buffer = []
    return counter, buffer