import json                     # to deserialze list
import motor                    # control the motor on car

def soc():
    import socket               # Import socket module
    import time
    from machine import Pin, TouchPad, PWM
    
    #servo pin setup
    p1 = Pin(13)
    servo = PWM(p1, freq=50)
    
    #socket setup
    s = socket.socket()         # Create a socket object
    host = 'Esp32 ip'           # esp32 ip on network
    port = 12345                # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    
    
    while True:
        c, addr = s.accept()    # Establish connection with client.
        print ('Got connection from', addr)
        
        while True:
            d = "thank you for connection"
            data = str(d)
            msg =str.encode(data, 'utf-8')
            c.send(msg)
            a = c.recv(1028)
            com = a.decode()       
            de = json.loads(com)#deserialze incoming dictionary
            
            if de["w"] == 1 and de["s"] == 0:
                motor.motorSpeed(-180)
            if de["s"] == 1 and de["w"] == 0:
                motor.motorSpeed(180)
            if de["a"] == 1 and de["d"] == 0:
                servo.duty(55)
            if de["d"] == 1 and de["a"] == 0:
                servo.duty(89)
            if de["d"] == 0 and  de["a"] == 0:
                servo.duty(75)
            if de["w"] == 0 and de["s"] == 0:
                motor.motorSpeed(0)
                
            #print(de) #for debugging
