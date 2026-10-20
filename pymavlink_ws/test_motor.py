import time
from pymavlink import mavutil

# 1. Connect to the flight controller
print("Connecting to Pixhawk...")
master = mavutil.mavlink_connection('/dev/ttyACM1', baud=115200)

# 2. Wait for heartbeat to establish communication
print("Waiting for heartbeat...")
master.wait_heartbeat()
print("Connection established!")

# 3. Send the Motor Test command
# Command ID: MAV_CMD_DO_MOTOR_TEST (209)
print("Sending command to spin Motor 1 for 3 seconds at 5% throttle...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,
    0,  # Confirmation
    4,  # Param 1: Motor instance (1 = Motor 1)
    0,  # Param 2: Throttle type (0 = Percentage)
    5,  # Param 3: Throttle value (5 = 5% power. Keep this low!)
    3,  # Param 4: Timeout in seconds (3 seconds)
    1,  # Param 5: Motor count (1 = test just this one motor)
    0,  # Param 6: Test order (0 = default)
    0   # Param 7: Not used
)

# 4. Wait for the flight controller to acknowledge the command
msg = master.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
if msg:
    print(f"Command Acknowledged. Result code: {msg.result}")
    # Result code 0 (MAV_RESULT_ACCEPTED) means success.
else:
    print("No acknowledgment received.")
