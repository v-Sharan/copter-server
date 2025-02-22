import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def camera_control(msg, cameraip):
    global sock
    sock.sendto(msg, ("100.78.80.27", 14550))
    return True
