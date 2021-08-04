import cv2
import numpy as np
import socket
from log import key_check
import os
import time
from alexnet import alexnet
s = socket.socket()         # Create a socket object
host = '192.168.137.142' # Get local machine name
port = 12345                # Reserve a port for your service.
s.connect((host, port))
cap = cv2.VideoCapture('http://192.168.137.221:81/stream')
#time.sleep(5)

last_pos = 0
w = 0
KP = 2
KD = 1.4
KI = .5
max_correction = 500

def convert(x, i_m, i_M, o_m, o_M):
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

def weighted(move):
    move.pop(1)
    avg_num = 0.0
    avg_den = 0.0
    for i in range(0,2):
        avg_num += move[i]*i*1000
        avg_den += move[i] 
    return avg_num/avg_den

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

WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'autonomous_car-{}-{}-{}-epochs.model'.format(LR, 'alexnetv2',EPOCHS)


def key_out(key):
    output = [0, 0, 0, 0]
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[2] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[3] = 1
    return output
    
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

while(True):
    
    ret, frame = cap.read()
    rotate = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    screen = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    #cv2.imshow('screen', screen)
    prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
    moves = list(np.around(prediction, decimals=2))
    w = convert(weighted(moves), 0, 1000, -500, 500)

    propotional_angle = int(w)
    derivative_angle = int(w) - last_pos
    integral_angle = int(w) + last_pos
    steer = (propotional_angle*KP + derivative_angle*KD + integral_angle*KI)
    z = int(correction(steer))
    st = servo_angle(z)
    x = '{"a":'
    x += str(st)
    x += ',"w":'
    x += str(1)
    x += "}"
    msg = str.encode(x, 'utf-8')
    print(msg)
    s.send(msg)
    data1 = s.recv(1024)
    last_pos = int(w)
    
    #a.pop()
    #print(a)
    #training_data.append([screen, a])
    #cv2.imshow('rotate', rotate)
    #blur = cv2.blur(rotate,(5,5))
    #edges = cv2.Canny(blur,150,200)
    

    
    print(moves, prediction)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()