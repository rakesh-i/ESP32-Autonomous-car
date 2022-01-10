import cv2
import numpy as np
import socket
from log import key_check
import os
import time
from alexnet import alexnet


s = socket.socket()         # Create a socket object
host = '192.168.1.110'    
port = 12345                # Reserve a port for your service.
s.connect((host, port))
cap = cv2.VideoCapture('http://192.168.1.104/stream') #esp32cam ip
#time.sleep(5)

WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'autonomous_car-{}-{}-{}-epochs.model'.format(LR, 'alexnet',EPOCHS)
    
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

while(True):
    ret, frame = cap.read()
    rotate = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    screen = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    #cv2.imshow('screen', screen)
    prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
    moves = list(np.around(prediction))
    x = '{"a":'
    x += str(moves[0])
    x += ',"d":'
    x += str(moves[2])
    x += ',"w":'
    x += str(1)
    x += ',"s":'
    x += str(0)
    x += "}"
    msg = str.encode(x, 'utf-8')
    #print(msg)
    s.send(msg)
    data1 = s.recv(1024)
    #print(moves, prediction)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
