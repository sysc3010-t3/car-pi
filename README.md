# RC Camera Car Mounted Pi Code

This is the repository for the software running on the mounted Raspberry Pi on
the cars in the RC Camera Car system. This repository contains the Python code
for a UDP client/server that uses a single port for communication. This code
base provides the behaviour for receiving control messages for moving the car
and controlling the headlights (server behaviour), as well as connecting to the
system's central server for initial registration and connection (client
behaviour). This component of the system communicates with an Arduino over a
serial connection and creates an HTTP web server for streaming a live video feed
from a Raspberry Pi Camera Module. This repository also contains configuration
files and shell scripts for configuring the Raspberry Pi to provide a wireless
access point, while still acting as wireless client. This code and configuration
has been developed and tested to run on the Raspbian operating system.

## Setup
### Dependencies:
* Python 3
  * pyserial
  * picamera
* hostapd
* dnsmasq

### Steps:
1. Set up the hardware.  
  a) Connect a Raspberry Pi Camera Module to the Raspberry Pi's Camera Serial
  Interface port.  
  b) Follow the instructions
  [here](https://www.raspberrypi.org/documentation/configuration/camera.md) to
  enable camera support.  
  c) Connect an Arduino to one of the Raspberry Pi's USB ports to allow for a
  serial connection between the two devices.  
2. Set up the Raspberry Pi as a wireless access point.  
  a) Follow the instructions
  [here](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md).  
  b) Copy the files in `config-files` to their corresponding locations, as
  indicated in `config-files/README.md`.  
  c) Reboot the Raspberry Pi.  
3. Run the car server.  
  a) Python 3 should come pre-installed on Raspbian.  
  b) Install the Python dependencies by running `pip3 install pyserial picamera`.  
  c) Run `sudo python3 main.py 5005`. The server will now be listening on port
     5005 for UDP requests from apps.  

## Code Structure
* [server.py](./server.py): class defining the general UDP server logic for
receiving and sending
* [handlers.py](./handlers.py): functions defining how the server will handle
all the different message types it receives and how it will send messages as a
client
* [main.py](./main.py): entrypoint for running the server; creates an instance
of the `Server` class
* [streaming.py](./streaming.py): code for setting up an HTTP web server to host
the live video stream from the camera feed
* [utils.py](./utils.py): general utility classes and functions
* [tests/](./tests/): location of test code
* [config-files/](./config-files/): configuration files for setting up the
Raspberry Pi as a wireless access point and a wireless client
* [shell-scripts/](./shell-scripts/): scripts for configuring the access point
and managing Wi-Fi networks/connections
