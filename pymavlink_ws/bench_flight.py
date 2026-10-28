import time
from pymavlink import mavutil

print("Connecting to Pixhawk...")
master = mavutil.mavlink_connection('/dev/ttyACM1', baud=115200)
master.wait_heartbeat()
print("Connection established!")

def set_throttle(pwm_value):
    """
    Sends an RC override command.
    Channels: 1:Roll, 2:Pitch, 3:Throttle, 4:Yaw
    A value of 0 means "release control back to the physical radio".
    """
    master.mav.rc_channels_override_send(
        master.target_system,
        master.target_component,
        0, 0, pwm_value, 0, 0, 0, 0, 0
    )
    print(f"Throttle set to {pwm_value / 10 - 100} %")

# 1. Switch to STABILIZE mode (Mode 0 in ArduCopter)
print("Setting STABILIZE mode...")
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    0
)
time.sleep(1)

# 2. Arm the vehicle
# Command ID: MAV_CMD_COMPONENT_ARM_DISARM (400), Param 1: 1 = Arm, 0 = Disarm
print("Arming motors...")
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0
)

# Wait a moment for motors to start spinning at idle speed
time.sleep(2) 

# 3. Simulate "Lift-off" (Ramp up throttle)
print("Throttling up...")
for pwm in range(1000, 1500, 10):
    set_throttle(pwm)
    # The loop delay dictates the speed of the throttle ramp. 
    # MAVLink requires these messages at ~10Hz minimum so it doesn't trigger a timeout.
    time.sleep(0.1) 

# 4. Hold at mid-throttle for 3 seconds
for i in reversed(range(3)):
    set_throttle(1500)
    print(f"Holding at mid-throttle...{i+1}")
    time.sleep(1)

# 5. Simulate "Landing" (Ramp down throttle)
print("Throttling down...")
for pwm in range(1500, 1000, -10):
    set_throttle(pwm)
    time.sleep(0.1)

# Release the throttle override entirely
print("Releasing throttle...")
set_throttle(1000)
time.sleep(1)

# 6. Disarm the vehicle
print("Disarming...")
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 0, 0, 0, 0, 0, 0, 0
)

print("Bench test complete.")
