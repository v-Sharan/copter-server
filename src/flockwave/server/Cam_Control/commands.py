# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# def camera_control(msg, cameraip):
#     global sock
#     sock.sendto(msg, (cameraip, 14551))
#     return True

# except zoom_in,zoom_out,zoom_stop
# packets = bytes.fromhex(stop)

# for zoom_in,zoom_out,zoom_stop
# packet = bytearray(zoom_in)
# bytePacket = bytes(packet)

Left = "EB 90 14 55 AA DC 11 30 01 F8 30 00 00 00 00 00 00 00 00 00 00 00 E8 2D"
right = "EB 90 14 55 AA DC 11 30 01 07 D0 00 00 00 00 00 00 00 00 00 00 00 F7 EB"
up = "EB 90 14 55 AA DC 11 30 01 00 00 07 D0 00 00 00 00 00 00 00 00 00 F7 EB"
down = "EB 90 14 55 AA DC 11 30 01 00 00 F8 30 00 00 00 00 00 00 00 00 00 E8 2D"
stop = "EB 90 14 55 AA DC 11 30 01 00 00 00 00 00 00 00 00 00 00 00 00 00 20 3D"
zoom_in = [235, 144, 6, 129, 1, 4, 7, 39, 255, 179]
zoom_out = [235, 144, 6, 129, 1, 4, 7, 55, 255, 195]
zoom_stop = [235, 144, 6, 129, 1, 4, 7, 0, 255, 140]
Take_picture = "EB 90 14 55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 04 D0 00 00 00 FA F9"
start_record = "EB 90 14 55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 05 10 00 00 00 3B 7B"
stop_record = "EB 90 14 55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 05 50 00 00 00 7B FB"
start_tracking = (
    "EB 90 14 55 AA DC 11 30 06 00 00 00 00 00 00 00 00 00 00 00 03 00 24 49"
)
stop_tracking = (
    "EB 90 14 55 AA DC 11 30 01 00 00 00 00 00 00 00 00 00 00 01 01 00 20 3F"
)
header = "EB 90"
point_to_track = "55 AA DC 0D 31 00 00 00 00 00 0A"
EO_IR_WhiteHot = (
    "EB 90 14 55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 03 83 00 00 00 AE 5F"
)
EO_IR_BlackHot = (
    "EB 90 14 55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 03 C3 00 00 00 EE DF"
)
EO_IR_PseudoColor = (
    "EB 90 14 55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 04 83 00 00 00 A9 5B"
)
Center_gimbal = (
    "EB 90 14 55 AA DC 11 30 04 00 00 00 00 00 00 00 00 00 00 00 00 00 25 45"
)
