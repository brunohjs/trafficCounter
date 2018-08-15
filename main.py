#!/usr/bin/env python
#coding: utf-8

import detect
import draw
import cartesian

import numpy as np
import cv2
import sys
import time


VIDEO_SOURCE = sys.argv[1]
MIN_AREA = 250
MAX_DISTANCE = 20

MEDIA_BLUR = 7
BLUR = 7

SENSIBILITY = 10
N_FRAMES_OUT = 15
FRAMES_LEARN = 100

'Parâmetros que definem as linhas de contagem da estrada'
'Padrão: [(x1, y1), (x2, y2)]'
ROAD_LINE_LEFT = [(60, 180), (210, 180)]
ROAD_LINE_RIGHT = [(210, 180), (350, 180)]

'Função de aprendizado do background'
def learnSub(backsub, video_source, n_frames=50):
    capture = cv2.VideoCapture(VIDEO_SOURCE)
    while capture.isOpened():
        ret, frame = capture.read()
        bkframe = backsub.apply(frame, None, 0.01)
        if capture.get(1) == n_frames:
            capture.release()
            break
    return bkframe
    
'Logger do buffer'
def logger(buffer, frame_id, count_left, count_right):
    print('Left: ', count_left)
    print('Right: ', count_right)
    print('Total: ', count_left+count_right)
    print('Frame: ', frame_id)
    for v in buffer:
        print(v, cartesian.distance(v['centroid'], (0,0)))
    print('\n')

'Função principal'
def main():
    buffer_vehicles = list()
    vehicle_counter_left = 0
    vehicle_counter_right = 0

    backsub = cv2.bgsegm.createBackgroundSubtractorMOG(nmixtures=3)
    bkframe = learnSub(backsub, VIDEO_SOURCE, FRAMES_LEARN)
    capture = cv2.VideoCapture(VIDEO_SOURCE)
    width = int(capture.get(3))
    

    #Trecho de código utilizado para os testes de entrada

    if 'video.mp4' in VIDEO_SOURCE:
        ROAD_LINE_LEFT = [(60, 180), (210, 180)]
        ROAD_LINE_RIGHT = [(210, 180), (350, 180)]
    elif 'video2.mp4' in VIDEO_SOURCE:
        ROAD_LINE_LEFT = [(0, 220), (175, 220)]
        ROAD_LINE_RIGHT = [(175, 220), (350, 220)]
    elif 'video3.mp4' in VIDEO_SOURCE:
        ROAD_LINE_LEFT = [(0, 220), (170, 220)]
        ROAD_LINE_RIGHT = [(170, 220), (350, 220)]
    elif 'video4.mp4' in VIDEO_SOURCE:
        ROAD_LINE_LEFT = [(0, 200), (180, 200)]
        ROAD_LINE_RIGHT = [(180, 200), (350, 200)]


    cv2.namedWindow('Background')
    cv2.moveWindow('Background', 400, 0)
    cv2.namedWindow('Track')

    while True:
        try:
            frame_id = int(capture.get(1))
            ret, frame = capture.read()
            
            bkframe = backsub.apply(frame, None, 0.01)
            bkframe = cv2.medianBlur(bkframe, MEDIA_BLUR)
            bkframe = cv2.blur(bkframe, (BLUR,BLUR))

            num, labels, stats, centroids = cv2.connectedComponentsWithStats(bkframe, ltype=cv2.CV_16U)
            count_left, count_right, buffer_vehicles, frame = detect.detectVehicle(
                stats, 
                centroids, 
                frame, 
                frame_id, 
                buffer_vehicles,
                ROAD_LINE_LEFT,
                ROAD_LINE_RIGHT)
            
            vehicle_counter_left += count_left
            vehicle_counter_right += count_right
            logger(buffer_vehicles, frame_id, vehicle_counter_left, vehicle_counter_right)
            
            draw.drawPanel(
                frame,
                ROAD_LINE_LEFT,
                ROAD_LINE_RIGHT,
                vehicle_counter_left,
                vehicle_counter_right,
                width
            )
            
            cv2.imshow('Track', frame)
            cv2.imshow('Background', bkframe)

            #cv2.imwrite('img/normal/background/'+str(frame_id)+'f.png', bkframe)

            if cv2.waitKey(100) == ord('q') or not capture.isOpened():
                break
        except Exception as e:
            print(e)
            break

    count_left, count_right, buffer_vehicles = detect.countVehicles(buffer_vehicles, frame_id, MAX_DISTANCE, N_FRAMES_OUT, final=True)
    vehicle_counter_left += count_left
    vehicle_counter_right += count_right
    logger(buffer_vehicles, frame_id, vehicle_counter_left, vehicle_counter_right)

if __name__ == '__main__':
    main()