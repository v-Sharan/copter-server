# import math

# Given values
# mass = 1  # kg
# gravity = 9.81  # m/s^2
# air_density = 1.225  # kg/m^3
# drag_coefficient = 1  # dimensionless
# cross_sectional_area = 0.0046  # m^2

# Terminal velocity formula
# terminal_velocity = math.sqrt(
#     (2 * mass * gravity) / (air_density * drag_coefficient * cross_sectional_area)
# )
# print(terminal_velocity)
from pymavlink import mavutil

master = mavutil.mavlink_connection("udpin:172.24.192.1:14551")

while True:
    msg = master.recv_match()
    if not msg:
        continue
    if msg.get_type() == "WIND":
        print(msg)
        # if msg.direction < 0:
        #     print(msg.direction + 360)
        # else:
        #     print(msg.direction)
