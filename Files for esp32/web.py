# setting up wireless connection
def connect():
    import network
    import time
    import machine
    #wifi credentials
    ssid = "YourSSID"
    password =  "YourPassword"
 
    station = network.WLAN(network.STA_IF)
    
    if station.isconnected() == True:
        print("Already connected")
        return
    station.active(True)
    if machine.reset_cause() != machine.SOFT_RESET:
        # configuration below MUST match your home router settings!!
        # CHECK DHCP RANGE OF YOUR ROUTER BEFORE ASSIGNING STATIC IP!!
        station.ifconfig(('static ip you want to assign', 'subnet mask', 'host ip', 'dns server')) 
        #example: station.ifconfig(('192.168.180.180', '255.255.255.9', '192.168.180.1', '8.8.8.8'))
        #if you are using laptop as access point: station.ifconfig(('static ip you want to assign', 'subnet mask', 'host ip', 'host ip'))
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
    print("Connection successful")
    
    #turn on onboard led for 5 sec to notify the successful connection
    from machine import Pin
    p = Pin(2, Pin.OUT)
    print(station.ifconfig())
    p.on()
    time.sleep(5)
    p.off()