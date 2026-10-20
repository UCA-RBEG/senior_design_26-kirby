import time
from pymavlink import mavutil

# 1. CONNECT TO THE FLIGHT CONTROLLER
# You can use '/dev/ttyACM1' (your USB connection) or '/dev/ttyAMA0' (your GPIO wiring)
# Make sure the baud rate matches what we set in QGroundControl (115200)
print("Connecting to Pixhawk...")
master = mavutil.mavlink_connection('/dev/ttyACM1', baud=115200)

# 2. WAIT FOR HEARTBEAT
print("Waiting for heartbeat...")
master.wait_heartbeat()
print(f"Target system {master.target_system}, target component {master.target_component} connected!")

# 3. SEND A COMMAND (Change Mode to GUIDED)
# GUIDED mode is MAV_MODE_FLAG_CUSTOM_MODE_ENABLED (custom mode 4 for ArduCopter)
print("Switching to GUIDED mode...")
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    4 # 4 is ArduCopter's GUIDED mode ID
)

# 4. READ INCOMING TELEMETRY (Main Loop)
print("Reading Attitude data (Press Ctrl+C to stop)...")
try:
    while True:
        # recv_match filters the incoming stream for a specific message type.
        # blocking=True means the script will pause here until an ATTITUDE message arrives.
        msg = master.recv_match(type='ATTITUDE', blocking=True)
        
        if not msg:
            continue
            
        # Convert radians to degrees for easier reading
        import math
        roll_deg = math.degrees(msg.roll)
        pitch_deg = math.degrees(msg.pitch)
        
        print(f"Roll: {roll_deg:.2f} | Pitch: {pitch_deg:.2f}")
        time.sleep(0.1) # Read 10 times a second

except KeyboardInterrupt:
    print("Exiting...")
