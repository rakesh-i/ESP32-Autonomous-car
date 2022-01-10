import socket               # Import socket module
import time
import json
from linuxLog import key_check



s = socket.socket()         # Create a socket object
host = '192.168.1.110'      # esp32 ip
port = 12345                # Reserve a port for your service.
s.connect((host, port))
#a = 'b'

try:
    while True:
        a = key_check()
        x = '{"a":'
        x += str(a[0])
        x += ',"d":'
        x += str(a[2])
        x += ',"w":'
        x += str(a[1])
        x += ',"s":'
        x += str(a[3])
        x += "}"
        msg = str.encode(x, 'utf-8')
        print(msg)
        s.send(msg)
        data1 = s.recv(1024)

except KeyboardInterrupt:
    print('exit')
    pass

 
