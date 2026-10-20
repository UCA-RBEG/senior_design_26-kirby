# senior_design_2627-kirby

## Flight Controller Info
Hardware: Pixhawk 6C
Firmware: ArduPilot(ArduCopter) 4.7.0
Communication: USB

## Get Started
### 1. Test with MAVProxy (tested on Ubuntu 26.04)
```console
sudo apt update
sudo apt install python3-pip
pip3 install mavproxy --break-system-packages
```
After connecting the Pi to the Flight Controller through USB C, run this:
```console
mavproxy.py --master=/dev/ttyACM0 --baudrate 115200  # FC could be assigned to ttyACM1 
```
An example outcome:
```console
Connect /dev/ttyACM1 source_system=255
Log Directory: 
Telemetry log: mav.tlog
Waiting for heartbeat from /dev/ttyACM1
MAV> AP: GCS Failsafe Cleared
Detected vehicle 1:1 on link 0
online system 1
STABILIZE> Mode STABILIZE
fence present
AP: ArduCopter V4.7.0 (1511f271)
AP: ChibiOS: 4f34e217
AP: Pixhawk6C-bdshot 003A0025 30345116 39393334
AP: IOMCU: 410 2003 411FC231
AP: RCOut: PWM:1-16
AP: IMU0: fast sampling 2.0kHz/2.0kHz
AP: Frame: QUAD/X
Received 1068 parameters (ftp)
Saved 1068 parameters to mav.parm
Flight battery 100 percent
```
### 2. PyMAVLink tests
Install from [PyMAVLink](https://github.com/ArduPilot/pymavlink) official repository.
- [Communication test](pymavlink_ws/test_comm.py)
- [Motor test](pymavlink_ws/test_motor.py)

## Old Things
To run the colordetection.py: 

    ros2 launch realsense2_camera rs_launch.py

On a separate terminal: 

    ros2 run kirbyros colordetection
    
