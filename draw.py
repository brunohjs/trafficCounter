#!/usr/bin/env python
#coding: utf-8

import cv2

def drawPanel(frame, road_left, road_right, count_left, count_right, width):
    
    cv2.line(frame, road_left[0], road_left[1], (100,255,0), 3)
    cv2.rectangle(frame, (0,0), (30,30), (230, 255, 180), -1)
    cv2.rectangle(frame, (0,0), (30,30), (100,255,0), 2)
    cv2.putText(frame,'%2r' %count_left, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (70,225,0), 2)
    
    cv2.line(frame, road_right[0], road_right[1], (0,130,255), 3)
    cv2.rectangle(frame, (width-30,0), (width,30), (80,210,255), -1)
    cv2.rectangle(frame, (width-30,0), (width,30), (0,130,255), 2)
    cv2.putText(frame,'%2r' %count_right, (width-25, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,130,255), 2)


def drawArea(frame, stat, centroid, area, color=(0,255,255)):
    initial_point = (stat[cv2.CC_STAT_LEFT], stat[cv2.CC_STAT_TOP])
    final_point = (initial_point[0] + stat[cv2.CC_STAT_WIDTH], initial_point[1] + stat[cv2.CC_STAT_HEIGHT])
    cv2.rectangle(frame, initial_point, final_point, (0, 0, 255), 1)
    cv2.circle(frame, centroid, 3, color, -1)