#!/usr/bin/env python
#coding: utf-8

import main
import cv2
import draw
from cartesian import distance

def detectVehicle(stats, centroids, frame, frame_id, buffer, road_line_left, road_line_right):
    n_left = 0
    n_right = 0
    for i in range(1, len(stats)):
        stat = stats[i]
        area = stat[cv2.CC_STAT_AREA]
        centroid = (int(centroids[i][0]), int(centroids[i][1]))
        if area >= main.MIN_AREA:
            draw.drawArea(frame, stat, centroid, area, (62,253,220))
            if inLine(road_line_left, centroid, main.SENSIBILITY):
                draw.drawArea(frame, stat, centroid, area, (251,66,27))
                buffer.append({
                    'id': frame_id,
                    'centroid' : centroid,
                    'area' : area,
                    'route' : 'L'
                })
            elif inLine(road_line_right, centroid, main.SENSIBILITY):
                draw.drawArea(frame, stat, centroid, area, (251,66,27))
                buffer.append({
                    'id': frame_id,
                    'centroid' : centroid,
                    'area' : area,
                    'route' : 'R'
                })
        
    if buffer:
        n_left, n_right, buffer = countVehicles(buffer, frame_id, main.MAX_DISTANCE, main.N_FRAMES_OUT)

    return n_left, n_right, buffer, frame

def inLine(road_line, point, sensibility=10):
    in_x = road_line[0][0] < point[0] < road_line[1][0] 
    in_y = (road_line[0][1]-sensibility) <= point[1] <= (road_line[1][1]+sensibility)
    if in_x and in_y:
        return True
    else:
        return False

def countVehicles(buffer, current_frame_id, max_distance=30, n_frames=15, final=False):
    count_left = 0
    count_right = 0
    i = 0
    while i < len(buffer)-1:
        j = i+1
        while j <= len(buffer)-1:
            near = distance(buffer[i]['centroid'], buffer[j]['centroid']) <= max_distance
            same = abs(buffer[i]['id'] - buffer[j]['id']) <= 5
            if near and same:
                del(buffer[i])
                break
            else:
                j += 1
        i += 1

    for vehicle in buffer:
        if abs(vehicle['id'] - current_frame_id) >= n_frames:
            if vehicle['route'] == 'L':
                count_left += 1
            else:
                count_right += 1 
            buffer.remove(vehicle)
    
    if final:
        for vehicle in buffer:
            if vehicle['route'] == 'L':
                count_left += 1
            else:
                count_right += 1 
        buffer = []
    
    return count_left, count_right, buffer