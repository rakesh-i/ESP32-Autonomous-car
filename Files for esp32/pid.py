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
    host = '192.168.1.110'    # Get local machine name
    port = 12345                # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    
    def convert(x, i_m, i_M, o_m, o_M):
        return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)
    
    
    def con():
    	motor.motorSpeed(0)
	while True:
	    c, addr = s.accept()    # Establish connection with client.
	    print ('Got connection from', addr)
	    
		    
	    while True:
		d = "thank you for connection"
		data = str(d)
		msg =str.encode(data, 'utf-8')
		try:
		    c.send(msg)
		    a = c.recv(1024)
		    com = a.decode()       
		    de = json.loads(com)#deserialze incoming dictionary

		    angle = int(de['a'])
		    speed = int(de["w"])
		    servo.duty(angle)
		    print(angle, speed)
		    if abs(speed):
			motor.motorSpeed(speed)
		    #if speed < 0:
		    #	motor.motorSpeed(speed)
		    else:
			motor.motorSpeed(0)
				    
		except:
		    con()
     
    con()    
				    #print(de) #for debugging
