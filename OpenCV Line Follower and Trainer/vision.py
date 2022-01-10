import cv2
import numpy as np
import time
import os 
import socket

cap = cv2.VideoCapture('http://192.168.0.104:81/stream')

while True:
    l = 0
    r = 0
    ret, frame = cap.read()
    rotate = cv2.rotate(frame, cv2.ROTATE_180)
    #screen = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
    #kernel = np.ones((10,10), np.float32)/225
    #smoothed = cv2.filter2D(rotate, -1, kernel)
    smoothed = cv2.medianBlur(rotate, 15)
    #edges = cv2.Canny(screen,100,200)
    low_b = np.uint8([60, 60, 60])
    high_b = np.uint8([0, 0, 0])
    mask = cv2.inRange(smoothed, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours)> 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #print("CX : "+str(cx)+"  CY : "+str(cy))
          
            
            
            cv2.circle(mask, (cx,cy), 5, (0 , 0, 255), -1)
    else :
        print("I don't see the line")
    cv2.drawContours(rotate, contours, -1, (0,255,0), 1)
    #cv2.imshow("gray", screen)
    #cv2.imshow('frame2', rotate)
    cv2.imshow('mask', mask)
    cv2.imshow('smooth', smoothed)
    #cv2.imshow("canny", edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
