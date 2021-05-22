### Setting up the wireless connection:
1. Type your router's SSID and password here in web.py file.
    ```sh
    ssid = "YourSSID"
    password =  "YourPassword"
    ```
2. Assigning the static ip, so you dont have to search esp32's ip everytime. Follow below example and do necessary changes in web.py.
    ```sh
    # configuration below MUST match your home router settings!!
    # CHECK DHCP RANGE OF YOUR ROUTER BEFORE ASSIGNING STATIC IP!!
    station.ifconfig(('static ip you want to assign', 'subnet mask', 'host ip', 'dns server')) 
    #example: station.ifconfig(('192.168.180.180', '255.255.255.9', '192.168.180.1', '8.8.8.8'))
    #if you are using laptop as access point: station.ifconfig(('static ip you want to assign', 'subnet mask', 'host ip', 'host ip'))
    ```
3. In server.py and command_server.py you need to type the static ip you assigned to the ESP32 here
   ```sh
   host = '111.111.111.111'    # esp32's ip on network
   ```
   check router's main menu to confirm esp32 is connected.
4. Now for client side add ip of esp32 here in client.py.
    ```sh
    host = '111.111.111.111'    # ESP32 ip
    ```
