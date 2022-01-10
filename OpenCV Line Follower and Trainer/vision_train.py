import cv2
import numpy as np
import time
import os 
import socket

s = socket.socket()         # Create a socket object
host = '192.168.1.110'      # Get local machine name
port = 12345                # Reserve a port for your service.
s.connect((host, port))

print('start')
file_name = 'training_data.npy'
if os.path.isfile(file_name):
    print("File exists , loading previous data")
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('file does not exist, starting fresh')
    training_data = []

speed = 1000                #range 0 to 1000

last_pos = 0
w = 0
KP = 2
KD = 1.4
KI = .5
max_correction = 1000

def convert(x, i_m, i_M, o_m, o_M):
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

def correction(angle):
    if angle > 0:
        if angle > max_correction:
            angle = max_correction
        else:
            angle = angle
    else:
        if angle < -max_correction:
            angle = -max_correction
        else:
            angle = angle 
    return angle

def servo_angle(z):
    if z > 0:
        steer_angle = convert(z, 0, 1000, 75, 89)
    else:
        steer_angle = convert(z, -1000, 0, 59, 75)
    return steer_angle


cap = cv2.VideoCapture('http://192.168.1.104:81/stream')

while True:
    l = 0
    r = 0
    ret, frame = cap.read()
    #rotate = cv2.rotate(frame, cv2.ROTATE_180)
    screen = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    kernel = np.ones((15,15), np.float32)/225
    smoothed = cv2.filter2D(frame, -1, kernel)
    #edges = cv2.Canny(screen,100,200)
    low_b = np.uint8([55, 55, 55])
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
            w = convert(cx, 0, 300, -500, 500)
            propotional_angle = int(w)
            derivative_angle = propotional_angle - last_pos
            integral_angle = propotional_angle + last_pos
            steer = (propotional_angle*KP + derivative_angle*KD + integral_angle*KI)
            z = int(correction(steer))
            st = servo_angle(z)
            x = '{"a":'
            x += str(st)
            x += ',"w":'
            x += str(speed)
            x += "}"
            msg = str.encode(x, 'utf-8')
            #print(msg)
            s.send(msg)
            data1 = s.recv(1024)
            last_pos = propotional_angle
            a = [0, 0, 0]
            if st > 78:
                a = [0, 1, 1]
            if st < 72:
                a = [1, 1, 0]
            if st>72 and st<78:
                a = [0, 1, 0]
            training_data.append([screen, a])
            #cv2.circle(mask, (cx,cy), 5, (0 , 0, 255), -1)
            #print(st, a)
            if len(training_data) % 500 == 0:
                print(len(training_data))
                np.save(file_name, training_data)
    else :
        print("I don't see the line")
        x = '{"a":'
        x += str(75)
        x += ',"w":'
        x += str(0)
        x += "}"
        msg = str.encode(x, 'utf-8')
        #print(msg)
        s.send(msg)
        data1 = s.recv(1024)
    #cv2.drawContours(frame, contours, -1, (0,255,0), 1)
    #cv2.imshow("gray", screen)
    #cv2.imshow('frame2', rotate)
    #cv2.imshow('mask', mask)
    #cv2.imshow('smooth', smoothed)
    #cv2.imshow("canny", edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("QUIT")
        x = '{"a":'
        x += str(75)
        x += ',"w":'
        x += str(0)
        x += "}"
        msg = str.encode(x, 'utf-8')
        #print(msg)
        s.send(msg)
        data1 = s.recv(1024)
        break

cap.release()
cv2.destroyAllWindows()
