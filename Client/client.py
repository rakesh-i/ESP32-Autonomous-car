import socket               # Import socket module
import time
from pynput.keyboard import Listener
import json
from log import key_check



s = socket.socket()         # Create a socket object
host = '192.168.137.142' # Get local machine name
port = 12345                # Reserve a port for your service.
s.connect((host, port))
#a = 'b'

def key_out(key):
    output = [0, 0, 0, 0]
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[3] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[2] = 1
    return output


while True:
    key = key_check()
    a = key_out(key)
    x = '{"a":'
    x += str(a[0])
    x += ',"d":'
    x += str(a[3])
    x += ',"w":'
    x += str(a[1])
    x += ',"s":'
    x += str(a[2])
    x += "}"
    #print(x)
    #da = json.dumps(x)
    #a = input("anagle :")
    #data = a
    msg = str.encode(x, 'utf-8')
    print(msg)
    s.send(msg)
    data1 = s.recv(1024)
    #b = int(data1.decode())
    #print(b)
    #if b < 200:
    #    data = str(a)
    #    msg =str.encode(data, 'utf-8')
    #    s.send(msg)
    #else:
    #    c = 1
    #    data2 = str(c)
    #    msg2 = str.encode(data2, 'utf-8')
    #    s.send(msg2)
    #time.sleep()

 